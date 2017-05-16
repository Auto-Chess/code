import os
import binascii
from datetime import datetime, timedelta

from flask import Flask, jsonify
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

    @staticmethod
    def clean_old():
        # Get all ChessBoards that haven't been used in a day, and delete
        old_date = datetime.today() - timedelta(days=1)
        print("Looking for ChessBoards older than {} to remove".format(old_date))

        old = ChessBoard.query.filter(ChessBoard.last_used < old_date).all()
        for board in old:
            print("Deleting board: {}".format(board))
            db.session.delete(board)

            # Delete moves
            i = 0
            for move in board.chess_moves:
                db.session.delete(move)
                i += 1

            if i > 0:
                print("    Delete {} child ChessMoves".format(i))

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

    def __init__(self, id, inital_col, initial_row, final_col, final_row):
        self.id = id

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
@app.route("/register")
def api_register():
    board = ChessBoard()
    db.session.add(board)
    db.session.commit()

    return jsonify({
        'board': board.serialize(),
        'errors': []
    })




# Run if not being included
if __name__ == "__main__":
    ChessBoard.clean_old()
    app.run()
