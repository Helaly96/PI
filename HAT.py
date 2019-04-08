import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

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
        
        self.Max_Magazine = 1
        self.Zero_Magazine= 0
        self.Min_Magazine = -1

        self.Enable = False
        self.pilot_enable = False

        self.channel_micro = 3
        self.zero_micro = 0
        self.forward_micro = 4000

        # for Magazine
        self.IN1 = 20 
        self.IN2 = 21
        self.ENA = 16
        self.ENA_PWM = 0

        # for Pulley 
        self.IN3 = 26
        self.IN4 = 19
        self.ENB = 13
        self.ENB_PWM = 0

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)

        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        self.micro_gpio = 24
        GPIO.setup(self.micro_gpio, GPIO.OUT)

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

    def Magazine_Servo(self):
        # take action when pulley is stoped
        if self.ENB_PWM == 0:
            pwm = self._devices['Magazine_Servo']['current']
            if pwm == self.Max_Magazine:
                GPIO.output(self.ENA, 1)
                GPIO.output(self.IN1, 1)
                GPIO.output(self.IN2, 0)
                self.ENA_PWM = 1

            elif pwm == self.Zero_Magazine:
                GPIO.output(self.ENA, 0)
                GPIO.output(self.IN1, 0)
                GPIO.output(self.IN2, 0)
                self.ENA_PWM = 0

            elif pwm == self.Min_Magazine:
                GPIO.output(self.ENA, 1)
                GPIO.output(self.IN1, 0)
                GPIO.output(self.IN2, 1)
                self.ENA_PWM = 1

        else :
            self._devices['Magazine_Servo']['current'] = self.Zero_Magazine
            GPIO.output(self.ENA, 0)
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 0)
            self.ENA_PWM = 0
            print("Stop Magazine from Magazine El72 el DC Chopper ya Sa3eeeed")

    def _updatePWM(self,pwms:dict):
        for device_name in pwms:
            # Check for PID Mode Controlled By Pilot ==================================
            if self.pilot_enable:
                # Check for PID Enable Controlled by Equation
                if ( device_name == "Vertical_Right" or device_name == "Vertical_Left" ) and self.Enable == True:
                    continue
             # ========================================================================
            # Check for Repetetion
            if self._devices[device_name]['current'] == pwms[device_name]:
                continue

            self._devices[device_name]['current'] =pwms[device_name]

            if device_name == 'Magazine_Servo':
                self.Magazine_Servo()
                continue

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
            GPIO.output(self.micro_gpio,pwm)
            print("Micro GPIO ",pwm)

    def Pulley(self,pwm):
        if self._devices['Magazine_Servo']['current'] != self.Zero_Magazine or self.ENA_PWM == 1:           

            self._devices['Magazine_Servo']['current'] = self.Zero_Magazine
            GPIO.output(self.ENA, 0)
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 0)
            self.ENA_PWM = 0
            print("Stop Magazine from Pulley El72 el DC Chopper ya Sa3eeeed")

        if pwm == 0:
            GPIO.output(self.ENB, 0)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 0)
            self.ENB_PWM = 0            

        elif pwm == 1:
            GPIO.output(self.ENB, 1)
            GPIO.output(self.IN3, 1)
            GPIO.output(self.IN4, 0)
            self.ENB_PWM = 1      

        elif pwm == -1:
            GPIO.output(self.ENB, 1)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)
            self.ENB_PWM = 1      
        
        print("ENB PWM",self.ENB_PWM)

    def Clean_GPIO(self):
            
            GPIO.output(self.ENA, 0)
            GPIO.output(self.ENB, 0)

            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 1)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)

            GPIO.output(self.micro_gpio,0)
            print("HARD CLEAN GPIO")

    def update(self, event_name,pwm):

        if event_name == "HAT":
            self._updatePWM(pwm)

        if event_name == "PID":
            self.PID_Control(pwm)

        if event_name == "Micro_ROV":
            self.Micro_ROV(pwm=pwm)

        if event_name == "Pulley":
            self.Pulley(pwm=pwm)

        if event_name == "Clean_GPIO":
            self.Clean_GPIO()

    def PID_Control(self, pwm):
        if self.Enable:
            if abs ( self._devices['Vertical_Left']['current'] - pwm ) <= 1:
                return

            self._hat.set_pwm(self.channelZ1,0,int(pwm))
            time.sleep(self.delay)
            self._hat.set_pwm(self.channelZ2,0,int(pwm))
            time.sleep(self.delay)

            self._devices['Vertical_Left']['current'] =int(pwm)
            self._devices['Vertical_Right']['current'] =int(pwm)

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
