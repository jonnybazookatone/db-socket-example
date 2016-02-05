import app
from views import socketio
from models import db, Thingy
from flask import url_for, current_app
from flask.ext.testing import TestCase


class TestSocketApp(TestCase):

    def create_app(self):
        app_ = app.create_app()
        return app_

    def setUp(self):
        db.create_all()
        self.io_client = socketio.test_client(self.app, namespace='/test')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.io_client.disconnect()

    def test_socketio_on_db_event(self):
        """
        Test that the WebSocket emits a signal when there is an update to the
        database
        """
        emitted = self.io_client.get_received('/test')
        self.assertIn(
            'Connected: nothing new for utcnow:',
            emitted[0]['args'][0]['data']
        )

        url = url_for('update')
        r = self.client.get(url)
        self.assertEqual(r.data, 'updated')

        emitted = self.io_client.get_received('/test')
        thingy = db.session.query(Thingy).first()

        expected_text = 'update <User 1, {}, {}>'\
            .format(thingy.date_created, thingy.date_last_modified)

        self.assertEqual(
            expected_text,
            emitted[0]['args'][0]['data']
        )
