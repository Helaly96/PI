
# raspberryyyyyyyyyyyyyyyyyyyyyyyyyy 22222222
class Hat:
    def __init__(self, address, frequency):
        self.address = address
        self.frequency = frequency

        self._devices = {}
    # Set the Speed of All Motors
    def add_Device(self,name,channel,zero_value):
        self._devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}
        print('device: ',self._devices[name],' added at channel',self._devices[name]['channel'])

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
        #print(pwms)
    def update(self, event_name,pwm):

        if event_name == "PWM":
            self._updatePWM(pwm)
