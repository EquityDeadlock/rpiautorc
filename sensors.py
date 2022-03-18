from abc import ABC, abstractmethod
import json, subprocess
class Sensor(ABC):
    def __init__(self):
        self.__data: str = None
        self.__prev_data = None

    @abstractmethod
    def getData(self) -> json:
        pass

class Ultrasonic(Sensor):
    def __init__(self):
        super().__init__()

    def getData(self) -> json:
        return ""

class MotorController(Sensor):
    def getData(self) -> json:
        return ""

class Accelerometer(Sensor):
    def __init__(self):
        super().__init__()

    def __readData(self):
        self.__data = subprocess.Popen("sudo ./adx -f 1 -t 1 | head -n 1", shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    def __delimitData(self) -> [str]:
        return self.__data.split(",")
    def getData(self) -> json:
        self.__readData()
        fields = self.__delimitData()
        return {"time":fields[0],"x":fields[1], "y":fields[2], "z":fields[3]}
