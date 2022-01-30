from flask import Flask,  render_template

from utils import ROOT_DIR

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
