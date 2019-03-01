import threading
class Sensor:
    def __init__(self,time):
        self.pwm = 305
        self.pressure = 0
        self.time = time

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal

    def interrupt(self, update, name):
#        self.update_pressure()
        update(name,self.pressure)
        threading.Timer(self.time, self.interrupt, [update, name]).start()

    def update_pressure(self):
        self.pressure += 1
    def update_pwm(self,event,z:int):
#        if event == "SENSOR":
            self.pwm = z
#            print("Sensor: ",self.pwm)
