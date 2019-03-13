class Hat:
    def __init__(self, address, frequency,delay):
        self.address = address
        self.frequency = frequency
        self.emit_signal = None
        self._devices = {}
    # Set the Speed of All Motors
    def add_Device(self,name,channel,zero_value):
        self._devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}
        print('device: ',name,self._devices[name])

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal

    # pwms is a dict ======> {'Motor1' : value1 , 'Motor2 : value2 ,.... etc }
    def _updatePWM(self,pwms:dict):
        for device_name in self._devices:
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue
            self._devices[device_name]['current'] =pwms[device_name]
#        print(pwms)

    def update(self, event_name,pwm):

        if event_name == "HAT":
            self._updatePWM(pwm)
#            self.emit_signal("SENSOR",pwm['Vertical_Right'])
        if event_name == "HATs":
            print(pwm)
