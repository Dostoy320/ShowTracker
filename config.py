import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tracker.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
DATABASE = 'showtracker/tmp/tracker.db'
DEBUG = True
SECRET_KEY = 'temp key'
USERNAME = 'admin'
PASSWORD = 'default'
