from flask.ext.socketio import emit

from . import io


@io.on('broadcast')
def broadcast(message):
    emit('broadcast', message, broadcast=True)
