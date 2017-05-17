import os
import binascii
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autochess.db'
db = SQLAlchemy(app)

# Models
# -- Define
class ChessBoard(db.Model):
    __tablename__ = 'chess_boards'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    secret = db.Column(db.String(64), nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)

    chess_moves = db.relationship('ChessMove', back_populates='chess_board')

    def __init__(self):
        self.secret = binascii.hexlify(os.urandom(32)).decode("utf-8")[:64]
        self.last_used = datetime.today()

    def __str__(self):
        return "<ChessBoard id={}, secret={}, chess_moves.len={}>".format(self.id, self.secret, len(self.chess_moves))

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            'id': self.id,
            'secret': self.secret,
            'last_used': self.last_used,
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

    initial_col = db.Column(db.String(1), nullable=False)
    inital_row = db.Column(db.Integer, nullable=False)

    final_col = db.Column(db.String(1), nullable=False)
    final_row = db.Column(db.Integer, nullable=False)

    def __init__(self, chess_board_id, inital_col, initial_row, final_col, final_row):
        self.chess_board_id = chess_board_id

        self.initial_col = inital_col
        self.inital_row = initial_row

        self.final_col = final_col
        self.final_row = final_row

    def __str__(self):
        return "<ChessMove id={}, chess_board_id={}, {}{}=>{}{}>".format(
            self.id,
            self.chess_board_id,
            self.initial_col, self.inital_row,
            self.final_col, self.final_row
        )

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            'id': self.id,
            'chess_board_id': self.chess_board_id,
            'inital_col': self.initial_col,
            'inital_row': self.inital_row,
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

# -- -- Register
@app.route("/chess_board/register")
def api_register():
    board = ChessBoard()
    db.session.add(board)
    db.session.commit()

    return jsonify({
        'board': board.serialize(),
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
            'errors': ["ChessBoard with id \"{}\" not found".format(chess_board_id)]
        }), 404)

    # Check ChessBoard secret
    chess_board_secret = request.headers['Authorization']
    if board.secret != chess_board_secret:
        return make_response(jsonify({
            'errors': ["ChessBoard secret in Authorization header does not match stored ChessBoard secret"]
        }), 401)

    # All good return None
    return None


@app.route("/chess_board/<id>/push_move", methods=['POST'])
def api_push_move(chess_board_id):
    # Check request
    err_resp = check_chess_board_secret(chess_board_id)
    if err_resp is not None:
        return err_resp

    # Check for required fields
    if ('initial_col' not in request.json) or \
        ('initial_row' not in request.json) or \
        ('final_col'  not in request.json) or \
        ('final_row' not in request.json):
        return make_response(jsonify({
            'errors': ["One or more of the required request fields was missing"]
        }), 400)

    # Make ChessMove
    board = ChessBoard.query.filter(id=chess_board_id).first()
    move = ChessMove(board.id, request.json.inital_col, request.json.inital_row
                     request.json.final_col, request.json.final_row)

    # Save
    db.session.add(move)
    db.session.commit()

# Run if not being included
if __name__ == "__main__":
    ChessBoard.clean_old()
    app.run()
