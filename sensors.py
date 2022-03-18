import json, subprocess, random
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

    def getData(self) -> json:
        if super()._isSimulation():
            return {"distance":super()._getRandomFloat(2.0, 30.0, 2)}
        else:
            return {"distance":0.0}



class MotorController(Sensor):
    def __init__(self, sim=False):
        super().__init__(sim)
    def getData(self) -> json:
        return ""

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
