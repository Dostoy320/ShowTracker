# imports
import sqlite3
from flask import Flask, g, abort
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from showtracker import views, models




if __name__ == '__main__':
    app.run()
