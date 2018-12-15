from Network import *
# from HAT import *
from DummyHat import *
from Equation_Motion import *
from Observer_Pattern import *
from Sensor import *
from DummySensor import *
from UDP import *

class ROV_19:

    def __init__(self):
        # ================= ROV System =========================
#        self.RaspberryPi_IP = '111.111.111.111'
#        self.Qt_IP = '111.111.111.112'
#        self.RaspberryPi_IP = '127.0.0.1'
        self.Qt_IP = '127.0.0.1'
        self.RaspberryPi_IP = '192.168.1.15'



        self.stream_IP = '111.111.111.100' #sink ( Laptop's address )
        self.Port = 8082
        self.stream_Ports = ['5022','','']
        self.UDP_IP = "127.0.0.1"
        self.UDP_Port = 5005
        self.Hat_address = 0x40
        self.Motors_Frequency = 50

        # Qt String .. 'x=0,y=100,r=0,z=0,Cam_H_Servo=0,Cam_V_Servo=0,Back_Cam=0,light=0,'
        # ========================================================

        self.selector =selectors.DefaultSelector()

        self.observer_pattern = Observer_Pattern()
        self.hat = Hat( self.Hat_address, self.Motors_Frequency)
        self.motion = Motion()
        self.tcp_server = TCP(self.selector,self.RaspberryPi_IP, self.Port, self.stream_IP ,self.stream_Ports )
        self.udp_client = UDP(self.UDP_IP ,self.UDP_Port)
#        self.sensor = Dummy_Sensor()

        self.hat.add_Device('Left_Front', 1, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Front', 2, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Back', 3,self.motion.Zero_thruster)
        self.hat.add_Device('Left_Back', 4, self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Right', 5, self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Left', 6, self.motion.Zero_thruster)
#        self.hat.add_Device('Cam_H_Servo', 7, self.motion.Zero_Servo)
#        self.hat.add_Device('Cam_V_Servo', 8, self.motion.Zero_Servo)
#        self.hat.add_Device('Back_Cam', 9, self.motion.Zero_Servo)
        self.hat.add_Device('Main_Cam',12,self.motion.Zero_Servo)
        self.hat.add_Device('light', 10, 0)

        self.motion.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.tcp_server.SIGNAL_Referance(self.observer_pattern.emit_Signal)

        self.observer_pattern.registerEventListener('PWM', self.hat.update)
        self.observer_pattern.registerEventListener('TCP', self.motion.update)
        self.observer_pattern.registerEventListener('TCP_ERROR', self.motion.update)
#        self.observer_pattern.registerEventListener('SENSOR',self.udp_client.update)

#        self.sensor.interrupt(self.observer_pattern.emit_Signal,'SENSOR')

        self.tcp_server.main_Loop()

Scarrlet = ROV_19()

