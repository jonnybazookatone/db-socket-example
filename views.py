from models import db, Thingy
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

socketio = SocketIO()


@db.event.listens_for(Thingy, 'after_insert')
def after_insert(mapper, connection, target):
    socketio.emit(
        'my response',
        {'data': 'update {}'.format(str(target))},
        namespace='/test'
    )


def index():
    return render_template('index.html')


def update():
    thingy = Thingy()
    db.session.add(thingy)
    db.session.commit()
    return 'updated'


@socketio.on('connect', namespace='/test')
def test_connect():
    """
    Check when the user connects if there is a new thingy
    """
    utcnow = datetime.utcnow()
    all_thingys = db.session.query(Thingy).filter(Thingy.date_last_modified > utcnow).all()

    if len(all_thingys) == 0:
        emit('my response', {'data': 'Connected: nothing new for utcnow: {}'.format(utcnow)})
    else:
        emit('my response', {'data': 'Connected: new thingies for utcnow: {}, {}'.format(utcnow, all_thingys)})
