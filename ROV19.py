from VideoStream import *
from Network import *
from Equation import *
from Observer_Pattern import *
from UDP import *
# from Sensor import *
from HAT import *
from DummySensor import *
#from DummyHat import *
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
        self.stream_Ports = ['5022','5000','10000']
        self.UDP_IP = self.Laptop_IP
        self.UDP_Port = 8005
        self.Hat_address = 0x40
        self.Motors_Frequency = 60
        self.Zero_Vertical = 400
        self.Qt_String = {'x':0,'y':100,'r':0,'z':0,'cam':0,'light':0}
        self.hat_delay = 0.000020 # us

        self.pipeline1 = "v4l2src device=/dev/video0 ! image/jpeg,width=1280,height=720,framerate=60/1 ! rtpjpegpay ! udpsink host=" + self.Laptop_IP + " port=" + self.stream_Ports[0]
        self.pipeline2 = "v4l2src device=/dev/video1 ! image/jpeg,width=1280,height=720,framerate=60/1 ! rtpjpegpay ! multiudpsink clients=" + self.Laptop_IP + ":" +self.stream_Ports[1] + "," + self.Laptop_IP + ":" + self.stream_Ports[2]
        # for Laptop's Camera
        # self.pipeline1 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5022"
        # self.pipeline2 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! multiudpsink clients=127.0.0.1:1234,127.0.0.1:5022"


        # Qt String .. x=0,y=100,r=0,z=0,Cam_H_Servo=0,Cam_V_Servo=0,Back_Cam=0,light=0,
        # Qt String .. x=0,y=100,r=0,z=0,cam=0,light=0,
        # ========================================================

        self.selector =selectors.DefaultSelector()

        self.tcp_server = TCP(self.selector,self.RaspberryPi_IP, self.Port, self.Laptop_IP ,self.stream_Ports )
        self.observer_pattern = Observer_Pattern()
        self.hat = Hat( self.Hat_address, self.Motors_Frequency,self.hat_delay)
        self.motion = Motion(self.Qt_String)
        self.udp_client = UDP(self.UDP_IP ,self.UDP_Port)
        self.sensor = Sensor(1.1)
        self.Camera = Gstreamer(self.pipeline1)
        self.Camera2 = Gstreamer(self.pipeline2)

        self.hat.add_Device('Left_Front', 7, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Front', 4, 400)
        self.hat.add_Device('Right_Back', 12,400)
        self.hat.add_Device('Left_Back',15 , 400)
        self.hat.add_Device('Vertical_Right', 8, 400)
        self.hat.add_Device('Vertical_Left', 10, 400)
        self.hat.add_Device('Main_Cam',0,400)
        self.hat.add_Device('Back_Cam',2,400)
        self.hat.add_Device('Magazine_Servo',3,1450)


        self.motion.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.tcp_server.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.hat.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.sensor.SIGNAL_Referance(self.observer_pattern.emit_Signal)

        self.observer_pattern.registerEventListener('HAT', self.hat.update)
        self.observer_pattern.registerEventListener('TCP', self.motion.update)
        self.observer_pattern.registerEventListener('TCP_ERROR', self.motion.update)
#        self.observer_pattern.registerEventListener('SENSOR', self.sensor.update_pwm)
        self.observer_pattern.registerEventListener('Sensor', self.tcp_server.update)

#        self.sensor.interrupt(self.observer_pattern.emit_Signal,'Sensor')

        self.main_Loop()

    def main_Loop(self):
        print('Wait for zeft Qt')
        while True:
            try:
                events = self.selector.select()
                for key, mask in events:
                    key.data()
            except KeyboardInterrupt:
                print(' Tari2 El Salama Enta')
                self.tcp_server.close()
                self.Camera.close()
                self.Camera2.close()
                return

ORCA = ROV_19()
