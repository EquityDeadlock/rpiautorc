from sensors import *
from database import *


fireDB = Database() # Database Object
Sensor.SIMULATE = False # Toggle all Sensors to simulated values

# Sensor Objects
ultra = Ultrasonic()
accel = Accelerometer()
motor = MotorController()

def main():
    while True:
        writeUltra()
        writeAccel()

def writeUltra(): 
    fireDB.setReference(Database.ULTRASONIC)
    fireDB.set(ultra.getData())
def writeAccel(): 
    fireDB.setReference(Database.ACCELEROMETER)
    fireDB.set(accel.getData())



if __name__ == "__main__":
    main()
