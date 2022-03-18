# motor.py

import RPi.GPIO as GPIO          
from time import sleep

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
print("\n")
print("The default speed & direction of motor is HIGH & Forward.")
print("r-run s-stop f-forward b-backward e-exit")
print("\n")    

# While loop to check state

def checkMotor():
    x = input()
    
    GPIO.output(21, GPIO.LOW)
    sleep(.25)
    GPIO.output(21, GPIO.HIGH)

    if x == 'r':
        print("run")

        if(temp1 == 1):
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


    elif x == 's':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

    elif x == 'f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        temp1 = 1

    elif x == 'b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp1 = 0
    
    elif x == 'e':
        GPIO.cleanup()
        print("GPIO clean up")
        
    
    else:
        print("Invalid input")

