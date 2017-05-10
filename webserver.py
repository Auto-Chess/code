from flask import Flask

# Flask app
app = Flask(__name__)

# Routes
# -- -- Index
@app.route("/")
def frontend():
    # Server static/index.html
    return app.send_static_file('index.html')

# Run if not being included
if __name__ == "__main__":
    app.run()