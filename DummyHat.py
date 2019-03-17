class Hat:
    def __init__(self, address, frequency,delay):
        self.address = address
        self.frequency = frequency
        self.emit_signal = None
        self._devices = {}

        self.Zero_Vertical=305
        self.channelZ1 = None
        self.channelZ2 = None
        self.Enable = False

    # Set the Speed of All Motors
    def add_Device(self,name,channel,zero_value):
        self._devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}
        print('device: ',name,self._devices[name])
        if name == "Vertical_Right":
            self.channelZ1 = channel
            print ("Channel Z =",self.channelZ1)
        elif name == "Vertical_Left":
            self.channelZ2 = channel
            print ("Channel Z =",self.channelZ2)

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal
    def Raspberry_pi_Power(self,channel,value):
        pass
    # pwms is a dict ======> {'Motor1' : value1 , 'Motor2 : value2 ,.... etc }
    def _updatePWM(self,pwms:dict):
        for device_name in self._devices:
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue
            self._devices[device_name]['current'] =pwms[device_name]
        print(pwms)

    def Enable_PID(self,value):
        self.Enable = value
        print("Enable: ",value)

    def update(self, event_name,pwm):

        if event_name == "HAT":
            self._updatePWM(pwm)

        if event_name == "PID":
            self.PID_Control(pwm)

    def PID_Control(self, pwm):
        if self.Enable:
            print ("PID,Control :",pwm)

