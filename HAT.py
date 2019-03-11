import Adafruit_PCA9685
import time

class Hat:
    def __init__(self, address, frequency,delay):
        self.address = address
        self.frequency = frequency
        self._hat = Adafruit_PCA9685.PCA9685()
        self._hat.set_pwm_freq(frequency)
        self.delay = delay
        self._devices = {}
        self.emit_signal =None
    # Set the Speed of All Motors
    def add_Device(self,name,channel,zero_value):
        self._devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}
        self._hat.set_pwm(channel,0,int(zero_value))

    def getDeviceBaseValue(self,device_name):
        return self._devices[device_name]['zero']
    def getDeviceValue(self,device_name):
        return self._devices[device_name]['current']
    def setDeviceValue(self, device_name,value):
        self._devices[device_name]['current'] = value

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal
#device_name == 'Vertical_Right' or device_name == 'Vertica_Left') and 
    # pwms is a dict ======> {'Motor1' : value1 , 'Motor2 : value2 ,.... etc }
    def _updatePWM(self,pwms:dict):
        for device_name in self._devices:
            # ======================== Check for Sudden Change =======================
            if( device_name == "Vertical_Right" or device_name == "Vertica_Left") and self._devices[device_name]['current'] != self._devices[device_name]['zero']
            and pwms[device_name] == self._devices[device_name]['zero']:
                for i in range 5 :
                    self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['zero'])
            # ========================================================================

            if self._devices[device_name]['current'] == pwms[device_name]:
                continue
            self._devices[device_name]['current'] =pwms[device_name]
            self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['current']))
            time.sleep(self.delay)
        print(pwms)
            if (self._devices[device_name]['current'] != self._devices[device_name]['zero']) and (pwms[device_name] == self._devices[device_name]['zero']):
                for i in range (5) :
                     self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['zero']) )
#                     time.sleep(0.020)
#            print ("Meaw")

            if (self._devices[device_name]['current'] == pwms[device_name]) :
                continue
            self._devices[device_name]['current'] =pwms[device_name]
            self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['current']))
            time.sleep(self.delay)
#        print(pwms)
    def update(self, event_name,pwm):

        if event_name == "HAT":
            self._updatePWM(pwm)
#            self.emit_signal("SENSOR",pwm['Vertical_Right'])
    
