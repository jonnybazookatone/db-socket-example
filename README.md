# Database event websocket example

Run the app
```python
python app.py
```

Access the webpage at localhost:5000. A websocket is opened to the backend service from the web interface. By pressing 'update' it makes
a commit to the SQL database in the backend. There is an SQLAlchemy event attached to the Thingy model, that when a commit is made to the
database it notifies the web app. The web app then generates a SocketIO signal that is emitted to the front end via the WebSocket.
