import time
import Adafruit_PCA9685

class Hat:
    def __init__(self, address, frequency,delay):
        self._hat = Adafruit_PCA9685.PCA9685()
        self._hat.set_pwm_freq(frequency)

        self.address = address
        self.frequency = frequency
        self.delay = delay
        self._devices = {}
        self.emit_signal =None
        self.Zero_Vertical=305
        self.channelZ1 = None
        self.channelZ2 = None
        self.Magazine_Channel = None
        self.Enable = False
        self.pilot_enable = False


        self.channel_micro = 3
        self.zero_micro = 0
        self.forward_micro = 4000

        self.channel_pulley = 4
        self.zero_pulley = 305
        self.pulley_forward = 400
        self.pulley_reverse = 200

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
        elif name == "Magazine_Servo":
            self.Magazine_Channel = channel
            print ("Magazine Channel :",self.Magazine_Channel)

    def Raspberry_pi_Power(self,channel,value):
        self._hat.set_pwm(channel,0,value)

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal



    def _updatePWM(self,pwms:dict):
        for device_name in pwms:
            # Check for PID Mode Controlled By Pilot ==================================
            if self.pilot_enable:
                # Check for PID Enable Controlled by Equation
                if ( device_name == "Vertical_Right" or device_name == "Vertical_Left" ) and self.Enable == True:
                    print ("Joystick can't change in Z")
                    continue
             # ========================================================================
            # Check for Repetetion
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue

            self._devices[device_name]['current'] =pwms[device_name]
            self._hat.set_pwm(self._devices[device_name]['channel'],0,int(self._devices[device_name]['current']))
            time.sleep(self.delay)
        print(pwms)

    def Pilot_Enable(self,event,enable):
        self.pilot_enable = enable
        if not self.pilot_enable :
            self._hat.set_pwm(self.channelZ1,0,self.Zero_Vertical)
            self._hat.set_pwm(self.channelZ2,0,self.Zero_Vertical)

    def Enable_PID(self,event,value):
        self.Enable = value

    def Micro_ROV(self,pwm):
        if pwm == 0:
            self._hat.set_pwm(self.channel_micro, 0, self.zero_micro)
        elif pwm == 1:
            self._hat.set_pwm(self.channel_micro, 0, self.forward_micro)

    def Pulley(self,pwm):
        if pwm == 0:
            self._hat.set_pwm(self.channel_pulley, 0, self.zero_pulley)
        elif pwm == 1:
            self._hat.set_pwm(self.channel_pulley, 0,self.pulley_forward )
        elif pwm == -1:
            self._hat.set_pwm(self.channel_pulley, 0,self.pulley_reverse )

    def update(self, event_name,pwm):

        if event_name == "HAT":
            self._updatePWM(pwm)

        if event_name == "PID":
            self.PID_Control(pwm)

        if event_name == "Micro_ROV":
            self.Micro_ROV(pwm=pwm)

        if event_name == "Pulley":
            self.Pulley(pwm=pwm)

    def PID_Control(self, pwm):
        if self.Enable:
            self._hat.set_pwm(self.channelZ1,0,int(pwm))
            self._hat.set_pwm(self.channelZ2,0,int(pwm))
            self._devices['Vertical_Left']['current'] =int(pwm)
            self._devices['Vertical_Right']['current'] =int(pwm)

#            print ("Z_pwm:",pwm)
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
