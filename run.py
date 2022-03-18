from sensors import *
from database import *

fireDB = Database() # Database Object
Sensor.SIMULATE = False
# Sensor Objects
ultra = Ultrasonic()
accel = Accelerometer()
motor = Motor()

def main():
    while True:
        checkSim()
        checkMotor()
        writeUltra()
        writeAccel()
        motor.checkMotor()

def writeUltra(): 
    fireDB.setReference(Database.ULTRASONIC)
    fireDB.set(ultra.getData())
def writeAccel(): 
    fireDB.setReference(Database.ACCELEROMETER)
    fireDB.set(accel.getData())
def checkSim():
    fireDB.setReference(Database.SIM)
    Sensor.SIMULATE = fireDB.get() # Toggle all Sensors to simulated values
def checkMotor():
    fireDB.setReference(Database.MOTOR_CONTROLLER)
    motor.state = fireDB.get()


if __name__ == "__main__":
    main()
