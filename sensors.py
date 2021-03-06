import json, subprocess, random
from turtle import distance
import RPi.GPIO as GPIO          
from time import sleep, time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 6
GPIO_ECHO = 22
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# GPIO pin numbers
in1 = 24
in2 = 23
in3 = 16
in4 = 12
en = 25
en2 = 20
temp1 = 1
# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p = GPIO.PWM(en,1000)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
o = GPIO.PWM(en2,1000)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21, GPIO.HIGH)

# Set pwm duty cycle
p.start(100)
o.start(100)
class Sensor:
    SIMULATE = False
    def __init__(self, sim=False):
        self.__data: str = None
        self.__sim = sim
        
    def _isSimulation(self) -> bool:
        return Sensor.SIMULATE or self.__sim

    def _getRandomFloat(self, minimum: float, maximum: float, decimalPlaces: int) -> float:
        return round(random.uniform(minimum, maximum), decimalPlaces)
    
class Ultrasonic(Sensor):
    def __init__(self, sim=False):
        super().__init__(sim)

        if super()._isSimulation():
            self.__minDistance = 2.0
            self.__maxDistance = 30.0
    
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
    
        StartTime = time()
        StopTime = time()
    
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time()
    
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def getData(self) -> json:
        if super()._isSimulation():
            return {"distance":super()._getRandomFloat(2.0, 30.0, 2)}
        else:
            return {"distance":self.distance()}

class Motor(Sensor):
    def __init__(self, sim=False):
        super().__init__(sim)
        self.state = "s"
        self.last = "s"
    def turnOff(self):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        self.state = "s"
    def getData(self) -> json:
        return {"state":self.state}
    def checkMotor(self):
        GPIO.output(21, GPIO.LOW)
        sleep(.25)
        GPIO.output(21, GPIO.HIGH)

        if self.state == "j":
            print("run")

            if(Motor.temp1 == 1):
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                print("forward")

            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                print("reverse")

            self.last = "j"


        elif self.state == 's':
            print("stop")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            self.last = "s"

        elif self.state == 'f':
            print("forward")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            Motor.temp1 = 1
            self.last = "f"

        elif self.state == 'b':
            print("backward")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            temp1 = 0
            self.last = "b"
        elif self.state == 'l':
            print("left")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            temp1 = 0
            self.last = "l"
        
        elif self.state == 'r':
            print("right")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            temp1 = 0
            self.last = "r"

        elif self.state == 'e':
            GPIO.cleanup()
            print("GPIO clean up")
            
        
        else:
            print("Invalid input")

class Accelerometer(Sensor):
    def __init__(self, sim=False):
        super().__init__(sim)
        
        self.__minTime: float = 0.0
        self.__maxTime: float = 1
        self.__minX: float = -10.0
        self.__maxX: float = 10.0
        self.__minY: float = -10.0
        self.__maxY: float = 10.0
        self.__minZ: float = -2.0
        self.__maxZ: float = 2.0
        self.__places: int = 1

    def __readData(self):
        self.__data = subprocess.Popen("sudo ./adx -f 1 -t 1 | head -n 1", shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    
    def __delimitData(self) -> [str]:
        return self.__data.split(",")
    
    def getData(self) -> json:
        if super()._isSimulation():
            time = super()._getRandomFloat(self.__minTime, self.__maxTime, self.__places)
            x = super()._getRandomFloat(self.__minX, self.__maxX, self.__places)
            y = super()._getRandomFloat(self.__minY, self.__maxY, self.__places)
            z = super()._getRandomFloat(self.__minZ, self.__maxZ, self.__places)
            return {"time":time,"x":x, "y":y, "z":z}
        else:
            self.__readData()
            fields = self.__delimitData()
            return {"time":float(fields[0]),"x":float(fields[1]), "y":float(fields[2]), "z":float(fields[3])}
