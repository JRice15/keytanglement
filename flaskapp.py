from flask import Flask,  render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room

from utils import ROOT_DIR
from client import generate_pairings_and_groupings

app = Flask(__name__)
with open("secret.key", "r") as f:
    app.config['SECRET KEY'] = f.read().strip()
socketio = SocketIO(app)

# def get_db():
#     if 'db' not in flask.g:
#         flask.g.db = sqlite3.connect(
#             flask.current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         flask.g.db.row_factory = sqlite3.Row

#     return flask.g.db

@app.route('/', methods=["POST", "GET"])
def room_select():
    if request.method == "POST":
        return redirect(url_for("room", roomname=request.form["roomname"]))
    return render_template("room_select.html")

@app.route('/room/<roomname>')
def room(roomname):
    return render_template("chat.html", room=roomname)

@socketio.on('message')
def handle_message(data):
    # show message to this user only
    emit("prepare message", data["user"])
    emit("status update", "Generating random pairings & groupings")
    user_pairings = generate_pairings_and_groupings(data["user"], 7*120)
    emit("status update", "Running quantum operations")
    
    quantum_computer
    emit("status update", "Comparing pairings & groupings with other user")
    key_generation
    emit("message", data)

# @socketio.on("join")
# def handle_join(data):
#     user = data["user"]
#     room = data["roomname"]
#     join_room(room)
#     emit("join notice", data["user"])



if __name__ == "__main__":
    socketio.run(app)
