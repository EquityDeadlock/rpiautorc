from abc import ABC, abstractmethod
class Sensor(ABC):
    @abstractmethod
    def readData() -> str:
        pass

class Ultrasonic(Sensor):
    def readData() -> str:
        pass
class MotorController(Sensor):
    def readData() -> str:
        pass
    
class Accelerometer(Sensor):
    def readData() -> str:
        pass
