from flask import Flask,  render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room

from utils import ROOT_DIR, AttackerError
from client import generate_pairings_and_groupings
from quantum_computer import quantum_compute
from key_generation import get_correct_measurements, check_for_eavesdropper, generate_code
from encrypt_decrypt import string_to_bits, encrypt, decrypt, bits_to_string
from bitarray import bitarray
import math
import string

app = Flask(__name__)
with open(ROOT_DIR + "secret.key", "r") as f:
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
    # filter for non-ascii
    message = "".join([letter for letter in data["message"] if string.printable])
    if not len(message):
        emit("bad message", data["user"])
        return
    
    bit_message = string_to_bits(message)

    emit("prepare message", {"user": data["user"], "msglen": str(len(bit_message))}, broadcast=True)

    needed_runs = math.ceil(len(bit_message) / 2) + 3

    emit("status update", "Generating random pairings & groupings")
    alice_data = generate_pairings_and_groupings(needed_runs)
    bob_data = generate_pairings_and_groupings(needed_runs)

    emit("status update", "Running quantum operations (takes a while)")
    alice_data, bob_data = quantum_compute(alice_data, alice_data)

    emit("status update", "Comparing pairings & groupings with other user")
    alice_correct, bob_correct = get_correct_measurements(alice_data, bob_data)

    emit("status update", "Checking for evidence of eavesdroppers")
    try:
        alice_correct, bob_correct = check_for_eavesdropper(alice_correct, bob_correct, 3)
    except AttackerError:
        emit("attacker", data["user"], broadcast=True)
        return 

    emit("status update", "Generating secure key")
    alice_code = generate_code(alice_correct["groupings"])
    bob_code = generate_code(bob_correct["groupings"])

    emit("status update", "Encrypting, sending, and decrypting")
    # encrypt with alice
    encrypted = encrypt(bit_message, bitarray(alice_code))
    # "sending"...
    # decrypt with bob
    decrypted = decrypt(encrypted, bitarray(bob_code))

    # return message
    data["message"] = bits_to_string(decrypted)
    emit("message", data, broadcast=True)

@socketio.on("join")
def handle_join(data):
    user = data["user"]
    room = data["roomname"]
    join_room(room)
    emit("join notice", data["user"], broadcast=True)



if __name__ == "__main__":
    socketio.run(app)
