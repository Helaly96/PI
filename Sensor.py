import threading
import ms5837

class Sensor_Interrupter :
    def __init__(self):
        self.pressure = 0
        self.sensor = ms5837.MS5837_30BA()
        self.time = 1

        if not self.sensor.init():
            print ("Sensor could not be initialized")
            exit(1)
        if not self.sensor.read():
            print ("Sensor read failed!")
            exit(1)

    def interrupt(self,update,name):
        self.update_pressure()
        update(name,self.pressure)
        threading.Timer(self.time,self.interrupt,[update,name]).start()

    def update_pressure(self):
        if self.sensor.read():
            self.pressure = self.sensor.pressure()


