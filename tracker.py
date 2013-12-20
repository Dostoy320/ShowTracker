# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# configuration 
# TODO: move configuration to own file
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'temp key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)