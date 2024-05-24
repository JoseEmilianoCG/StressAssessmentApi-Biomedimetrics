import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(current_dir, 'database', 'google-services.json')

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {'storageBucket':'**.appspot.com'})

source_blob_name = 'dummy.json'

db = firestore.client()

#def get_firebase_data():
