import os
import binascii
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, send, emit

from multiprocessing import Process

def random_string():
    return binascii.hexlify(os.urandom(32)).decode("utf-8")

# Flask app
app = Flask(__name__)
app_host = "127.0.0.1"
app_port = 5000

ENV_DEBUG = "debug"
ENV_PROD = "production"
ENV_TEST = "test"

ENVIRONMENT = os.getenv('ENVIRONMENT', ENV_DEBUG)

if ENVIRONMENT == ENV_TEST:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autochess.db'
elif ENVIRONMENT == ENV_DEBUG:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/auto-chess'
elif ENVIRONMENT == ENV_PROD:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://auto-chess:{}@localhost/auto-chess".format(os.getenv("DB_PASSWORD", "NO_PASSWORD"))
    app_host = "0.0.0.0"
    app_port = 80

app.config['SECRET_KEY'] = random_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
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
    turn_number = db.Column(db.Integer, nullable=False)

    TURN_USER = 'user'
    TURN_OPPONENT = 'opponent'

    chess_moves = db.relationship('ChessMove', back_populates='chess_board')

    def __init__(self):
        self.secret = random_string()[:64]
        self.set_last_used_to_now()

        self.set_unique_short_code()

        self.game_running = True
        self.turn = ChessBoard.TURN_USER
        self.turn_number = 0

    def __str__(self):
        return "<ChessBoard id={}, secret={}, last_used={}, short_code={}, game_running={}, turn={}, turn_number={}, chess_moves.len={}>"\
            .format(self.id,
                self.secret,
                self.last_used,
                self.short_code,
                self.game_running,
                self.turn,
                self.turn_number,
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
            board = ChessBoard.query.filter(ChessBoard.short_code==code).first()

            # If no board with code exit, else repeat
            if board is None:
                break

        # Set code
        self.short_code = code

    """Sets ChessBoard turn to the opposite of provide value
    If value is TURN_USER then turn will be set to TURN_OPPONENT and vice versa
    
    Args:
        - value (str): Value to set opposite of
        
    Raises:
        - ValueError: If value is not one of TURN_USER or TURN_OPPONENT
    """
    def set_turn_opposite_of(self, value):
        if (value != ChessBoard.TURN_USER) and (value != ChessBoard.TURN_OPPONENT):
            raise ValueError("value must be one of \"{}\" or \"{}\", was: \"{}\"".format(ChessBoard.TURN_USER, ChessBoard.TURN_OPPONENT, value))

        if value == ChessBoard.TURN_USER:
            self.turn = ChessBoard.TURN_OPPONENT
        else:
            self.turn = ChessBoard.TURN_USER

    def increment_turn_number(self):
        self.turn_number += 1

    def serialize(self):
        return {
            'id': self.id,
            'secret': self.secret,
            'last_used': self.last_used,
            'short_code': self.short_code,
            'game_running': self.game_running,
            'turn': self.turn,
            'turn_number': self.turn_number,
            'chess_moves': self.chess_moves
        }

    def insecure_serialize(self):
        moves = []
        for move in self.chess_moves:
            moves.append(move.serialize())

        return {
            'id': self.id,
            'last_used': str(self.last_used),
            'short_code': self.short_code,
            'game_running': self.game_running,
            'turn': self.turn,
            'turn_number': self.turn_number,
            'chess_moves': moves
        }

    def pub_to_websocket(self):
        socketio.emit("chess_board", self.insecure_serialize(), room=self.short_code)

    def delete(self, children=False):
        db.session.delete(self)

        if children:
            for move in self.chess_moves:
                db.session.delete(move)

    @staticmethod
    def clean_old():
        # Get all ChessBoards that haven't been used in a day, and delete
        old_date = datetime.today() - timedelta(days=1)
        print("ChessBoard: Sanitising Chess Boards older than: {}".format(old_date))

        old = ChessBoard.query.filter(ChessBoard.last_used < old_date).all()
        for board in old:
            print("ChessBoard: Deleting old Chess Board, board: {}".format(board))
            board.delete(children=True)

        print("ChessBoard: Committing old Chess Board deletion")
        db.session.commit()
        print("ChessBoard: Old Chess Board deletion success")

class ChessMove(db.Model):
    __tablename__ = 'chess_moves'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    chess_board_id = db.Column(db.Integer, db.ForeignKey('chess_boards.id'))
    chess_board = db.relationship('ChessBoard', back_populates='chess_moves')

    player = db.Column(db.String(12), nullable=False)
    turn_number = db.Column(db.Integer, nullable=False)

    initial_col = db.Column(db.String(1), nullable=False)
    initial_row = db.Column(db.Integer, nullable=False)

    final_col = db.Column(db.String(1), nullable=False)
    final_row = db.Column(db.Integer, nullable=False)

    def __init__(self, chess_board_id, player, turn_number, initial_col, initial_row, final_col, final_row):
        self.chess_board_id = chess_board_id

        self.player = player
        self.turn_number = turn_number

        self.initial_col = initial_col
        self.initial_row = initial_row

        self.final_col = final_col
        self.final_row = final_row

    def __str__(self):
        return "<ChessMove id={}, chess_board_id={}, player={}, turn_number={}, {}{}=>{}{}>".format(
            self.id,
            self.chess_board_id,
            self.player,
            self.turn_number,
            self.initial_col, self.initial_row,
            self.final_col, self.final_row
        )

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            'id': self.id,
            'chess_board_id': self.chess_board_id,
            'player': self.player,
            'turn_number': self.turn_number,
            'initial_col': self.initial_col,
            'initial_row': self.initial_row,
            'final_col': self.final_col,
            'final_row': self.final_row
        }

    def pub_to_websocket(self):
        socketio.emit("chess_move", self.serialize(), room=self.chess_board.short_code)

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

@app.route("/img/chess_piece.svg")
def img_chess_piece():
    return app.send_static_file("img/chess_piece.svg")

# -- -- Register
@app.route("/chess_board/register")
def api_register():
    board = ChessBoard()
    db.session.add(board)
    db.session.commit()

    print("API Chess Board Register: Registered Chess Board, board: {}".format(board))

    return jsonify({
        'chess_board': board.serialize(),
        'errors': []
    })

def check_chess_board_secret(id):
    # Check move given by JSON
    if request.json is None:
        return make_response(jsonify({
            'errors': ["JSON body required"]
        }), 400)

    # Check secret provided
    if 'Authorization' not in request.headers:
        return make_response(jsonify({
            'errors': ["ChessBoard secret must be provided in Authorization header"]
        }), 401)

    # Check ChessBoard exists
    board = ChessBoard.query.filter(ChessBoard.id==id).first()

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

@app.route("/chess_board/short_code/<chess_board_short_code>")
def api_chess_board_get_by_short_code(chess_board_short_code):
    # Get board
    board = ChessBoard.query.filter(ChessBoard.short_code == chess_board_short_code).first()

    # Check exists
    if board is None:
        return make_response(jsonify({
            'errors': ["No Chess Board with provided short code found"]
        }), 404)

    # Return
    return jsonify({
        'chess_board': board.insecure_serialize(),
        'errors': []
    })

@app.route("/chess_board/<chess_board_id>")
def api_chess_board_get(chess_board_id):
    # Get board
    board = ChessBoard.query.filter(ChessBoard.id == chess_board_id).first()

    # Check exists
    if board is None:
        return make_response(jsonify({
            'errors': ["No Chess Board with provided id found"]
        }), 404)

    # Return
    return jsonify({
        'chess_board': board.insecure_serialize(),
        'errors': []
    })

@app.route('/chess_board/<chess_board_id>/game_running', methods=["DELETE"])
def api_chess_board_game_running_delete(chess_board_id):
    # Check request
    err_resp = check_chess_board_secret(chess_board_id)
    if err_resp is not None:
        return err_resp

    # Get board
    board = ChessBoard.query.filter(ChessBoard.id == chess_board_id).first()

    # Check exists
    if board is None:
        return make_response(jsonify({
            'errors': ["No Chess Board with provided id found"]
        }), 404)

    # Set not running
    board.game_running = False

    print("API Chess Board: {}: Stop game running".format(chess_board_id))

    # Save
    db.session.add(board)
    db.session.commit()

    # Notify
    board.pub_to_websocket()

    return jsonify({
        'errors': []
    })

@app.route("/chess_board/<chess_board_id>/moves/<chess_move_player>")
def api_chess_board_moves_list(chess_board_id, chess_move_player):
    # Check player value is valid
    if chess_move_player != 'user' and chess_move_player != 'opponent':
        return make_response(jsonify({
            'errors': ["Move player must have value \"user\" or \"opponent\""]
        }), 400)

    # Get Moves
    moves = ChessMove.query.filter(ChessMove.chess_board_id == chess_board_id and ChessMove.player == chess_move_player).all()

    # Make moves a response
    resp = []
    for move in moves:
        resp.append(move.serialize())

    return jsonify({
        'moves': resp,
        'errors': []
    })

@app.route("/chess_board/<chess_board_id>/moves/<chess_move_player>", methods=['POST'])
def api_chess_board_moves_create(chess_board_id, chess_move_player):
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
    board = ChessBoard.query.filter(ChessBoard.id == chess_board_id).first()
    board.set_turn_opposite_of(chess_move_player)
    board.increment_turn_number()
    board.set_last_used_to_now()

    move = ChessMove(board.id, chess_move_player, board.turn_number, request.json['initial_col'], request.json['initial_row'],
                     request.json['final_col'], request.json['final_row'])

    print("API Chess Board: Id {}: Moves: Player {}: Received move: {}".format(chess_board_id, chess_move_player, move))

    # Save
    db.session.add(board)
    db.session.add(move)
    db.session.commit()

    # Notify web clients
    move.pub_to_websocket()
    board.pub_to_websocket()

    return jsonify({'errors': []})

# -- -- Web socket
@socketio.on("join")
def socket_on_join(data):
    # Check Short Code in request
    if 'chess_board_short_code' not in data:
        emit("join_failed", "No short code provided")
        return False

    short_code = data['chess_board_short_code']

    # Check Chess Board with short code exists
    board = ChessBoard.query.filter(ChessBoard.short_code==short_code).first()
    if board is None:
        print("Error: Socket On join: Failed to find Chess Board with short code: \"{}\"".format(short_code))
        emit("join_failed", "No Chess Board with short code provided")
        return False

    print("Socket On join: Website client subscribed with short code: \"{}\"".format(short_code))

    join_room(short_code)
    emit("joined")

def _run_webserver():
    ChessBoard.clean_old()

    try:
        socketio.run(app, host=app_host, port=app_port)
    except KeyboardInterrupt as e:
        print("Keyboard interrupted server")

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
    _run_webserver()
