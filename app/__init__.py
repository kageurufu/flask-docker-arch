from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy

from .config import get_config

app = Flask(__name__)

app.config.from_object(get_config())

db = SQLAlchemy(app)
io = SocketIO(app)
Bootstrap(app)

from . import controllers, sockets
