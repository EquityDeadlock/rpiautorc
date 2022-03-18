from sensors import *
from database import *

fireDB = Database() # Database Object
Sensor.SIMULATE = False
# Sensor Objects
ultra = Ultrasonic()
accel = Accelerometer()
motor = MotorController()

def main():
    while True:
        checkSim()
        writeUltra()
        writeAccel()


def writeUltra(): 
    fireDB.setReference(Database.ULTRASONIC)
    fireDB.set(ultra.getData())
def writeAccel(): 
    fireDB.setReference(Database.ACCELEROMETER)
    fireDB.set(accel.getData())
def checkSim():
    fireDB.setReference(Database.SIM)
    Sensor.SIMULATE = fireDB.get() # Toggle all Sensors to simulated values


if __name__ == "__main__":
    main()
