from sensors import *
from database import *

def main():
    fireDB = Database()
    fireDB.setReference("Accelerometer")
    
    accel = Accelerometer()
    fireDB.set(accel.getData())


if __name__ == "__main__":
    main()
