from reaction import Reaction
from flask import Flask, request, session
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from dotenv import load_dotenv
import database
from flask_session import Session

load_dotenv()

app = Flask(__name__, static_folder="../build", static_url_path="/")

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SECRET_KEY"] = "mysecret"

CORS(app)
Session(app)

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)


student_room_counts = {} #stores the number of students in each room
students_sid = set() #stores the socket id of all active students
studentCount = 0

database.initialise_database()
database.fetch_snapshot()

# When there is a 404, we send it to react so it can deal with it
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")


@app.route("/")
@cross_origin()
def index():
    return app.send_static_file("index.html")

@app.route("/api/create-snapshot")
@cross_origin()
def create_snapshot():

    database.create_new_snapshot()
    update_counts()
    reset_buttons()

    print("created snapshot")
    return None

def update_counts():
    for reaction in Reaction:
        update_reaction_count(reaction)

    # print("hi")
    emit("update students connected", {"count":studentCount})

def reset_buttons():
    emit("reset buttons", broadcast=True)

def in_room(room):
    return room in socketio.server.rooms(request.sid)

@app.route("/api/snapshots")
@cross_origin()
def get_snapshots():
    snapshots = database.find_snapshots()

    return {"snapshots":snapshots}

@socketio.on("connect")
def test_connect():
    print("connected")
    print(request.sid)
    # update_counts()

@socketio.on("disconnect")
def test_disconnect():
    if request.sid in students_sid:
        student_room_counts[session["room"]] -= 1
        emit("update students connected", {"count":student_room_counts[session["room"]]}, to=session["room"])

    print("disconnected")

@socketio.on("join")
def on_join(data):
    room = data['room']

    if data['type'] == "student":
        students_sid.add(request.sid)
        student_room_counts[room] += 1
        emit("update students connected", {"count":student_room_counts[room]}, to=room)

    # need to remember to remove these rooms from counts when meeting ended otherwise we
    # will have wrong data saved over

    if data['type'] == "teacher" and room not in student_room_counts:
        student_room_counts[room] = 0 # intialise the room to 0

    session["type"] = data["type"] # stores student or teacher
    session["room"] = room
    join_room(room)
    print("{} joined room".format(data["type"]))

@socketio.on("leave")
def on_leave(data):
    room = data['room']

    if request.sid in students_sid:
        student_room_counts[room] -= 1
        emit("update students connected", {"count":student_room_counts[room]}, to=room)
        students_sid.remove(request.sid)

    leave_room(room)
    session.pop("room") # since they have now left the meeting
    print("left room")

@socketio.on("add reaction")
def handle_reaction(reaction, room):
    sid = request.sid
    database.add_insight(reaction, room, sid)
    update_reaction_count(reaction, room)
    update_all_reactions(room)

@socketio.on("remove reaction")
def handle_reaction(reaction, room):
    sid = request.sid
    database.remove_insight(reaction, room, sid)
    update_reaction_count(reaction, room)
    update_all_reactions(room)
    
def update_reaction_count(reaction, room):
    emit(
        "update " + reaction, 
        {"count":database.count_active(reaction, room)}, 
        to=room)

def update_all_reactions(room):
    output = {}
    for reaction in Reaction:
        output[reaction] = database.count_active(reaction, room)
    emit("update all", output, to=room)

@app.route("/api/reaction-count", methods=['POST'])
@cross_origin()
def get_reaction_count():
        # also add room later on
        reaction = request.json["reaction"]
        room = request.json["room"]
        return {"count":database.count_active(reaction, room)}

@app.route("/api/student-count", methods=['POST'])
@cross_origin()
def get_student_count():
        room = request.json["room"]
        # weird bug where not initially initialised? will need to fix this
        if room in student_room_counts:
            count = student_room_counts[room]
        else:
            count = 0
        return {"count":count}

@app.route("/api/all_reactions", methods=['POST'])
@cross_origin()
def get_all_reactions():
        room = request.json["room"]
        output = {}
        for reaction in Reaction:
            output[reaction] = database.count_active(reaction, room)
        print (output)
        return output


@socketio.on("create snapshot")
def handle_message():
    database.create_new_snapshot(session["room"])
    # need to update counts now
    update_counts(session["room"])
    update_all_reactions(session["room"])
    #reset buttons
    socketio.emit("reset buttons", to=session["room"])

@socketio.on("leave comment")
def add_comment(comment, reaction, room):
    sid = request.sid
    database.add_comment(comment, reaction, room, sid)
    socketio.emit("update comments", to=room)
    return {"success":True}

@app.route("/api/get-comments", methods=['POST'])
@cross_origin()
def get_comments():
        room = request.json["room"]
        comments = database.get_current_comments(room)
        print(comments)
        return {"comments": comments}


# code stuff
@app.route("/api/new-code")
@cross_origin()
def get_new_code():
    code = database.get_new_code()
    return {"code":code}

@app.route("/api/is-code-active", methods=['POST'])
@cross_origin()
def is_code_active():
    code = request.json['code']
    return {"valid":database.is_active_code(code)}
    


if __name__ == "__main__":
    socketio.run()
