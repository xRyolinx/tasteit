from app import socketio, session, db, conn
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit


@socketio.on('connect')
def connect(data):
    print("connected!")
    
@socketio.on('join')
def on_join(id):
    print(id)
    if not id:
        return
    # get room id
    ids = [int(id), int(session['compte']['id'])]
    ids.sort()
    room = str(ids[0]) + str(ids[1])
    print(room)
    # join room
    session['compte']['room'] = room
    join_room(room)


@socketio.on('send')
def sendmsgsocket(data):
    print(data)
    
    # Id of logged account
    id = session['compte']['id']
    # Data sent
    id_destinataire = data.get('id_destinataire')
    msg = data.get('msg')
    
    # Send to db
    db.execute("INSERT INTO messages (id_sent, message, id_received) VALUES (%s, %s, %s)",
               (id, msg, id_destinataire))
    conn.commit()
    
    room = session['compte'].get('room')
    
    # send to rooms
    data = {
        'status' : True,
        'data' : [{
            'id_sent' : id,
            'message' : msg,
        }],
    }
    emit("receive", data, to=room)
    
@socketio.on('leave')
def on_leave():
    room = session['compte'].get('room')
    if room:
        leave_room(room)
        del session['compte']['room']
    
    
@socketio.on('disconnect')
def disconnect():
    on_leave()