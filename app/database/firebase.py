import os
import json
import pyrebase
from app.database.databaseconfig import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()