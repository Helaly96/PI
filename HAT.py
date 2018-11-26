import Adafruit_PCA9685


class Hat:
    def __init__(self, address, frequency):
        self.address = address
        self.frequency = frequency
        self._hat = Adafruit_PCA9685.PCA9685()
        self._hat.set_pwm_freq(frequency)

        self._devices = {}
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
    # pwms is a dict ======> {'Motor1' : value1 , 'Motor2 : value2 ,.... etc }
    def _updatePWM(self,pwms:dict):
        for device_name in self._devices:
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue
            self._devices[device_name]['current'] =pwms[device_name]
            self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['current']))

    def update(self, args_tuple):

        event_name = args_tuple[0]
        pwm = args_tuple[1]

        if event_name == "PWM":
            self._updatePWM(pwm)
