import os
import json
import pyrebase

current_dir = os.path.dirname(os.path.abspath(__file__))
serviceAccountKey = os.path.join(current_dir, 'database', 'serviceAccountKey.json')


databaseinfo_path = os.path.join(current_dir, 'database','databaseinfo.json' )

with open(databaseinfo_path) as databaseinfo_file:
    databaseinfo = json.load(databaseinfo_file)


config = {
  "apiKey": databaseinfo["apiKey"],
  "authDomain": databaseinfo['authDomain'],
  "databaseURL": databaseinfo['database_url'],
  "storageBucket": databaseinfo['storage_bucket'],
  "serviceAccount": serviceAccountKey
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()