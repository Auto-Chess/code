import os
import binascii

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

    chess_moves = db.relationship('ChessMove', back_populates='chess_board')

    def __init__(self):
        self.secret = str(binascii.hexlify(os.urandom(32))[:64])

    def __str__(self):
        return "<ChessBoard id={}, secret={}, chess_moves.len={}>".format(self.id, self.secret, len(self.chess_moves))

    def __repr__(self):
        return str(self)

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

    res = dict(
        board=str(board),
        errors=[]
    )
    return jsonify(res)


# Run if not being included
if __name__ == "__main__":
    app.run()