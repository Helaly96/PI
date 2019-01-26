#import pigpio
#pi = pigpio.pi()

class GPIO:
    def __init__(self,Zero,frequency):
        self.emit_signal= None
        self.Zero = Zero
        self.frequency = frequency
        self.pwm = self.Zero

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal

    def update(self,pwm):
        self.pwm = pwm
        print(self.pwm)
#        pi.hardware_PWM(18, self.frequancy, self.pwm)

    def gpio_clean(self):
        self.pwm=0
#        pi.hardware_PWM(18, self.frequancy, 0)
#        pi.stop()
        print ("clean gpio")

