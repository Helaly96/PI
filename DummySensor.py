import threading
class Dummy_Sensor:
    def __init__(self):
        self.pressure = 0
        self.time = 1

    def interrupt(self, update, name):
        self.update_pressure()
        update(name, self.pressure)
        threading.Timer(self.time, self.interrupt, [update, name]).start()

    def update_pressure(self):
        self.pressure += 1
