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

from flask import Flask
from views import socketio, index, update
from models import db


def create_app():
    """
    App factory
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/update', 'update', update)

    db.init_app(app)
    socketio.init_app(app, async_mode=async_mode)

    return app


if __name__ == '__main__':

    app = create_app()
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
