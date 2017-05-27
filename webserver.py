import os
import binascii
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_socketio import SocketIO, join_room, leave_room

from multiprocessing import Process

def random_string():
    return binascii.hexlify(os.urandom(32)).decode("utf-8")

# Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/auto-chess'
app.config['REDIS_URL'] = 'redis://:@localhost:6379/0'
app.config['SECRET_KEY'] = random_string()

db = SQLAlchemy(app)
redis_store = FlaskRedis(app)
socketio = SocketIO(app)

# Models
# -- Define
class ChessBoard(db.Model):
    __tablename__ = 'chess_boards'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    secret = db.Column(db.String(64), nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)

    short_code = db.Column(db.String(4), nullable=False)

    game_running = db.Column(db.Boolean, nullable=False)
    turn = db.Column(db.String(12), nullable=False)

    TURN_USER = 'user'
    TURN_OPPONENT = 'opponent'

    chess_moves = db.relationship('ChessMove', back_populates='chess_board')

    def __init__(self):
        self.secret = random_string()[:64]
        self.set_last_used_to_now()

        self.set_unique_short_code()

        self.game_running = True
        self.turn = ChessBoard.TURN_USER

    def __str__(self):
        return "<ChessBoard id={}, secret={}, last_used={}, short_code={}, game_running={}, turn={}, chess_moves.len={}>"\
            .format(self.id,
                self.secret,
                self.last_used,
                self.short_code,
                self.game_running,
                self.turn,
                len(self.chess_moves))

    def __repr__(self):
        return str(self)

    def set_last_used_to_now(self):
        self.last_used = datetime.today()

    def set_unique_short_code(self):
        # Loop unit unique
        code = None
        while True:
            # Generate new code
            code = random_string()[:4]

            # Find boards with code
            board = ChessBoard.query.filter(short_code=code).first()

            # If no board with code exit, else repeat
            if board is None:
                break

        # Set code
        self.short_code = code

    def serialize(self):
        return {
            'id': self.id,
            'secret': self.secret,
            'last_used': self.last_used,
            'short_code': self.short_code,
            'game_running': self.game_running,
            'turn': self.turn,
            'chess_moves': self.chess_moves
        }

    def delete(self, children=False):
        db.session.delete(self)

        if children:
            for move in self.chess_moves:
                db.session.delete(move)

    @staticmethod
    def clean_old():
        # Get all ChessBoards that haven't been used in a day, and delete
        old_date = datetime.today() - timedelta(days=1)
        print("Looking for ChessBoards older than {} to remove".format(old_date))

        old = ChessBoard.query.filter(ChessBoard.last_used < old_date).all()
        for board in old:
            print("Deleting board: {}".format(board))
            board.delete(children=True)

        print("Committing deletion")
        db.session.commit()

class ChessMove(db.Model):
    __tablename__ = 'chess_moves'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    chess_board_id = db.Column(db.Integer, db.ForeignKey('chess_boards.id'))
    chess_board = db.relationship('ChessBoard', back_populates='chess_moves')

    player = db.Column(db.String(12), nullable=False)

    initial_col = db.Column(db.String(1), nullable=False)
    inital_row = db.Column(db.Integer, nullable=False)

    final_col = db.Column(db.String(1), nullable=False)
    final_row = db.Column(db.Integer, nullable=False)

    def __init__(self, chess_board_id, player, inital_col, initial_row, final_col, final_row):
        self.chess_board_id = chess_board_id

        self.player = player

        self.initial_col = inital_col
        self.initial_row = initial_row

        self.final_col = final_col
        self.final_row = final_row

    def __str__(self):
        return "<ChessMove id={}, chess_board_id={}, player={}, {}{}=>{}{}>".format(
            self.id,
            self.chess_board_id,
            self.player,
            self.initial_col, self.inital_row,
            self.final_col, self.final_row
        )

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            'id': self.id,
            'chess_board_id': self.chess_board_id,
            'player': self.player,
            'initial_col': self.initial_col,
            'initial_row': self.inital_row,
            'final_col': self.final_col,
            'final_row': self.final_row
        }

# -- -- Create
db.create_all()

# Routes
# -- -- Index
@app.route("/")
def frontend():
    # Server static/index.html
    return app.send_static_file('index.html')

# -- -- Socket IO resources
@app.route("/js/socket.io.js")
def socketio_client_lib():
    return app.send_static_file("js/socket.io.js")

@app.route("/js/socket.io.js.map")
def socketio_client_lib_map():
    return app.send_static_file("js/socket.io.js.map")

# -- -- Register
@app.route("/chess_board/register")
def api_register():
    board = ChessBoard()
    db.session.add(board)
    db.session.commit()

    return jsonify({
        'chess_board': board.serialize(),
        'errors': []
    })

def check_chess_board_secret(id):
    # Check move given by JSON
    if request.json is None:
        return make_response(jsonify({
            'errors': ["Move was be provided in JSON format"]
        }), 400)

    # Check secret provided
    if 'Authorization' not in request.headers:
        return make_response(jsonify({
            'errors': ["ChessBoard secret must be provided in Authorization header"]
        }), 401)

    # Check ChessBoard exists
    board = ChessBoard.query.filter(id=id).first()

    if board is None:
        return make_response(jsonify({
            'errors': ["ChessBoard with id \"{}\" not found".format(id)]
        }), 404)

    # Check ChessBoard secret
    chess_board_secret = request.headers['Authorization']
    if board.secret != chess_board_secret:
        return make_response(jsonify({
            'errors': ["ChessBoard secret in Authorization header does not match stored ChessBoard secret"]
        }), 401)

    # All good return None
    return None

@app.route("/chess_board/<id>/push_move/<player>", methods=['POST'])
def api_push_move(chess_board_id, chess_move_player):
    # Check request
    err_resp = check_chess_board_secret(chess_board_id)
    if err_resp is not None:
        return err_resp

    # Check player value is valid
    if chess_move_player != 'user' and chess_move_player != 'opponent':
        return make_response(jsonify({
            'errors': ["Move player must have value \"user\" or \"opponent\""]
        }), 400)

    # Check for required fields
    if ('initial_col' not in request.json) or \
        ('initial_row' not in request.json) or \
        ('final_col' not in request.json) or \
        ('final_row' not in request.json):
        return make_response(jsonify({
            'errors': ["One or more of the required request fields was missing"]
        }), 400)

    # Make ChessMove
    board = ChessBoard.query.filter(id=chess_board_id).first()
    board.set_last_used_to_now()

    move = ChessMove(board.id, chess_move_player, request.json.inital_col, request.json.inital_row,
                     request.json.final_col, request.json.final_row)

    # Save
    db.session.add(board)
    db.session.add(move)
    db.session.commit()

@socketio.on('join')
def socket_on_join(data):
    join_room(data['room'])

@socketio.on('leave')
def socket_on_leave(data):
    leave_room(data['room'])

def _run_webserver():
    ChessBoard.clean_old()
    socketio.run(app)

_run_thread = None
def run_webserver_in_thread():
    global _run_thread
    _run_thread = Process(target=_run_webserver)
    _run_thread.start()

def stop_webserver_in_thread():
    global _run_thread
    if _run_thread is not None:
        _run_thread.terminate()
        _run_thread.join()
    else:
        raise RuntimeError("Server not running")

# Run if not being included
if __name__ == "__main__":
    #_run_webserver()
    run_webserver_in_thread()
    stop_webserver_in_thread()
