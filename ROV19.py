from Network import *
#from HAT import *
from DummyHat import *
from Equation_Motion import *
from Observer_Pattern import *
# from Sensor import *
from DummySensor import *
from UDP import *

class ROV_19:

    def __init__(self):
        # ================= ROV System =========================
        # For PI 19
        #self.RaspberryPi_IP = '111.111.111.111'
        #self.Qt_IP = '111.111.111.112'

        # For PI 19 Wifi
        #self.RaspberryPi_IP = '192.168.1.15'


        # For PI 18
        # self.RaspberryPi_IP = '10.0.1.55'
        # self.Qt_IP = '10.0.1.54'

#        For Local
        self.RaspberryPi_IP = '127.0.0.1'
        self.Qt_IP = '127.0.0.1'

        self.stream_IP = '10.0.1.54' #sink ( Laptop's address )
        self.Port = 9005
        self.stream_Ports = ['5022','1234','']
        self.UDP_IP = "127.0.0.1"
        self.UDP_Port = 5005
        self.Hat_address = 0x40
        self.Motors_Frequency = 50

        # Qt String .. x=0,y=100,r=0,z=0,Cam_H_Servo=0,Cam_V_Servo=0,Back_Cam=0,light=0,
        # Qt String .. x=0,y=100,r=0,z=0,cam=0,light=0,
        # ========================================================

        self.selector =selectors.DefaultSelector()

        self.observer_pattern = Observer_Pattern()
        self.hat = Hat( self.Hat_address, self.Motors_Frequency)
        self.motion = Motion()
        self.tcp_server = TCP(self.selector,self.RaspberryPi_IP, self.Port, self.stream_IP ,self.stream_Ports )
        self.udp_client = UDP(self.UDP_IP ,self.UDP_Port)
        self.sensor = Dummy_Sensor(1)
#        self.sensor = Sensor(1)

        self.hat.add_Device('Left_Front', 11, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Front', 5, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Back', 3,self.motion.Zero_thruster)
        self.hat.add_Device('Left_Back',9 , self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Right', 0, self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Left', 7, self.motion.Zero_thruster)
        self.hat.add_Device('Main_Cam',15,self.motion.Zero_Servo)
        self.hat.add_Device('light', 13, 0)

        #self.hat.add_Device('Cam_H_Servo', 7, self.motion.Zero_Servo)
        #self.hat.add_Device('Cam_V_Servo', 8, self.motion.Zero_Servo)
        #self.hat.add_Device('Back_Cam', 9, self.motion.Zero_Servo)

        self.motion.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.tcp_server.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.hat.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.sensor.SIGNAL_Referance(self.observer_pattern.emit_Signal)

        self.observer_pattern.registerEventListener('PWM', self.hat.update)
        self.observer_pattern.registerEventListener('TCP', self.motion.update)
        self.observer_pattern.registerEventListener('TCP_ERROR', self.motion.update)
        self.observer_pattern.registerEventListener('SENSOR', self.sensor.update_pwm)
        self.observer_pattern.registerEventListener('CSV', self.udp_client.update)

        self.sensor.interrupt(self.observer_pattern.emit_Signal,'CSV')

        self.tcp_server.main_Loop()





Scarrlet = ROV_19()

