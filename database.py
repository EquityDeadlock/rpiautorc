import firebase_admin, json
from firebase_admin import credentials, db

class Database:
    ULTRASONIC = "Ultrasonic"
    ACCELEROMETER = "Accelerometer"
    MOTOR_CONTROLLER = "Motor Controller/state"
    SIM = "Simulate/enabled"
    def __init__(self):
        self.__cred = firebase_admin.credentials.Certificate("serviceAccountKey.json")
        self.__default_app = firebase_admin.initialize_app(self.__cred, {"databaseURL":"https://autonomous-rc-default-rtdb.firebaseio.com/"})
    
    def setReference(self, reference: str):
        self.__ref = db.reference(f"/{reference}")

    def getReference(self, reference: str):
        return self.__ref.get()

    def push(self, data: json):
        self.__ref.push(data)
    
    def set(self, data: json):
        self.__ref.set(data)

    def get(self):
        return self.__ref.get()

    def update(self, findPair: json):
        temp_ref = self.__ref.get()
        #for key, value in temp_ref.items():
            #if(value
             #   self.__ref.child(key).update(newPair)
