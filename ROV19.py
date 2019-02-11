from VideoStream import *
from Network import *
from Equation_Motion import *
from Observer_Pattern import *
from UDP import *
# from Sensor import *
# from HAT import *
from DummySensor import *
from DummyHat import *
import selectors

class ROV_19:

    def __init__(self):
        # ================= ROV System =========================
        # For PI 19
        self.RaspberryPi_IP = '1.1.1.1'
        self.Laptop_IP = '1.1.1.2'

        # For Local
        # self.RaspberryPi_IP = '127.0.0.1'
        # self.Laptop_IP = '127.0.0.1' # sink ( Laptop's address )

        self.Port = 9005
        self.stream_Ports = ['5022','1234','']
        self.UDP_IP = self.Laptop_IP
        self.UDP_Port = 8005
        self.Hat_address = 0x40
        self.Motors_Frequency = 50
        self.Zero_Vertical = 305

        self.pipeline1 = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=" + self.Laptop_IP + " port=" + self.stream_Ports[0]
        self.pipeline2 = "v4l2src device=/dev/video1 ! image/jpeg, width=1280, height=720, framerate=60/1 ! rtpjpegpay ! multiudpsink clients=" + self.Laptop_IP + ":" +self.stream_Ports[0] + "," + self.Laptop_IP + ":" + self.stream_Ports[1]
        # for Laptop's Camera
        # self.pipeline1 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5022"
        # self.pipeline2 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! multiudpsink clients=127.0.0.1:1234,127.0.0.1:5022"


        # Qt String .. x=0,y=100,r=0,z=0,Cam_H_Servo=0,Cam_V_Servo=0,Back_Cam=0,light=0,
        # Qt String .. x=0,y=100,r=0,z=0,cam=0,light=0,
        # ========================================================

        self.selector =selectors.DefaultSelector()

        self.observer_pattern = Observer_Pattern()
        self.hat = Hat( self.Hat_address, self.Motors_Frequency)
        self.motion = Motion()
        self.tcp_server = TCP(self.selector,self.RaspberryPi_IP, self.Port, self.Laptop_IP ,self.stream_Ports )
        self.udp_client = UDP(self.UDP_IP ,self.UDP_Port)
        self.sensor = Sensor(1)
#        self.Camera = Gstreamer(self.pipeline1)

        self.hat.add_Device('Left_Front', 11, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Front', 5, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Back', 3,self.motion.Zero_thruster)
        self.hat.add_Device('Left_Back',9 , self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Right', 0, self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Left', 7, self.motion.Zero_thruster)
        self.hat.add_Device('Main_Cam',15,self.motion.Zero_Servo)
        self.hat.add_Device('light', 13, 0)

        # self.hat.add_Device('Cam_H_Servo', 7, self.motion.Zero_Servo)
        # self.hat.add_Device('Cam_V_Servo', 8, self.motion.Zero_Servo)
        # self.hat.add_Device('Back_Cam', 9, self.motion.Zero_Servo)

        self.motion.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.tcp_server.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.hat.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.sensor.SIGNAL_Referance(self.observer_pattern.emit_Signal)

        self.observer_pattern.registerEventListener('HAT', self.hat.update)
        self.observer_pattern.registerEventListener('TCP', self.motion.update)
        self.observer_pattern.registerEventListener('TCP_ERROR', self.motion.update)
        self.observer_pattern.registerEventListener('SENSOR', self.sensor.update_pwm)
        self.observer_pattern.registerEventListener('CSV', self.udp_client.update)

        self.sensor.interrupt(self.observer_pattern.emit_Signal,'CSV')

        self.main_Loop()

    def main_Loop(self):
        print('Wait for zeft Qt')
        while True:
            try:
                events = self.selector.select()
                for key, mask in events:
                    key.data()
            except KeyboardInterrupt:
                print(' End')
                self.tcp_server.close()
#                self.Camera.close()
                return






Scarrlet = ROV_19()
