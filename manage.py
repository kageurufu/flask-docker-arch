#!/usr/bin/env python2
from flask.ext.script import Manager

from app import app, io
from app.models import *

manager = Manager(app)


@manager.command
def runserver():
    app.debug = True
    io.run(app, use_reloader=True)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def recreate_db():
    drop_db()
    create_db()


@manager.shell
def shell_context():
    return {'app': app, 'db': db, 'io': io}


if __name__ == '__main__':
    manager.run()
