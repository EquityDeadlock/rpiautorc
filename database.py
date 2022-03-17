import firebase_admin, json
from firebase_admin import credentials, db

class Database:
    def __init__(self):        
        self.__cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
        self.__default_app = firebase_admin.initialize_app(self.__cred, {"databaseURL":"https://autonomous-rc-default-rtdb.firebaseio.com/"})
    
    def setReference(self, reference: str) -> str:
        self.__ref = db.reference(f"/{reference}")

    def push(self, data: json):
        self.__ref.push(data)


