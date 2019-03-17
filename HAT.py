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
        self.Zero_Vertical=305
        self.channelZ1 = None
        self.channelZ2 = None
        self.Enable = False

    # Set the Speed of All Motors
    def add_Device(self,name,channel,zero_value):
        self._devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}
        self._hat.set_pwm(channel,0,int(zero_value))
        if name == "Vertical_Right":
            self.channelZ1 = channel
            print ("Channel Z =",self.channelZ1)
        elif name == "Vertical_Left":
            self.channelZ2 = channel
            print ("Channel Z =",self.channelZ2)

    def Raspberry_pi_Power(self,channel,value):
        self._hat.set_pwm(channel,0,value)


    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal

    def _updatePWM(self,pwms:dict):
        for device_name in self.pwms:
            if ( device_name == "Vertical_Right" or device_name == "Vertical_Right" ) and self.Enable == True:
                print ("Joystick can't change in Z")
                continue
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue
            self._devices[device_name]['current'] =pwms[device_name]
            self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['current']))
            time.sleep(self.delay)
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
            self._hat.set_pwm(self.channelZ1,0,pwm)
            self._hat.set_pwm(self.channelZ2,0,pwm)

    def Autonomus(self,dir:str):
        pwm = {'Left_Front':305,'Right_Front':305,'Right_Back':305,'Left_Back':305,'Vertical_Right':305,'Vertical_Left':305}
        if dir == "left":
            pass
        elif dir == "right":
            pass
        elif dir == "up":
            pass
        elif dir == "down":
            pass
        self._updatePWM(pwm)