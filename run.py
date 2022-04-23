from sensors import *
from database import *
from threading import Thread

fireDB = Database() # Database Object
Sensor.SIMULATE = False
# Sensor Objects
ultra = Ultrasonic()
accel = Accelerometer()
motor = Motor()

def main():
    while True:
        checkSim()
        writeUltra()
        checkMotor()
        motor.checkMotor()
        writeAccel()
        print("Main")


def writeUltra():
    while True:
        fireDB.setReference(Database.ULTRASONIC)
        fireDB.set(ultra.getData())
        motor.state = motor.last
        sleep(0.25)
def writeAccel():
    while True:
        fireDB.setReference(Database.ACCELEROMETER)
        fireDB.set(accel.getData())
        sleep(1)
def checkSim():
    while True:
        fireDB.setReference(Database.SIM)
        Sensor.SIMULATE = fireDB.get() # Toggle all Sensors to simulated values
def checkMotor():
    while True:
        fireDB.setReference(Database.MOTOR_CONTROLLER)
        motor.state = fireDB.get()
        sleep(0.25)

def test():
    while 1:
        if (ultra.distance() <= 25):
            motor.turnOff()
        print("############")
        sleep(0.2)
  

if __name__ == "__main__":
    try:
        t1 = Thread(target=checkSim)
        t2 = Thread(target=writeUltra)
        t3 = Thread(target=checkMotor)
        t4 = Thread(target=motor.checkMotor)
        t5 = Thread(target=writeAccel)
        t6 = Thread(target=test)
        #t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t4.setDaemon(True)
        t5.setDaemon(True)
        t6.setDaemon(True)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
    except:
        print("failed")
