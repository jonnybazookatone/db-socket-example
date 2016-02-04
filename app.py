#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from datetime import datetime
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_sqlalchemy import SQLAlchemy
from models import db, Thingy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
db.init_app(app)
with app.app_context():
    db.create_all()

socketio = SocketIO(app, async_mode=async_mode)


@db.event.listens_for(Thingy, 'after_insert')
def after_insert(mapper, connection, target):
    socketio.emit(
        'my response',
        {'data': 'update {}'.format(str(target))},
        namespace='/test'
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update', methods=['GET'])
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


if __name__ == '__main__':
    socketio.run(app, debug=True)
