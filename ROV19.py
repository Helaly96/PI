import faulthandler; faulthandler.enable()

#from dummy_depth_pid import *
from depth_pid import *
from Timer import *
from VideoStream import *
from Network import *
from Equation import *
from Observer_Pattern import *
from UDP import *
#from Sensor import *
from HAT import *
from DummySensor import *
#from DummyHat import *
import selectors
import select
import sys


class ROV_19:

    def __init__(self):
        # ================= ROV System =========================
        # For PI 19
        self.RaspberryPi_IP = '10.1.1.15'
        self.Laptop_IP = '10.1.1.14'
#        import os
#        os.kill(os.getpid(),11)
        # For Local
#        self.RaspberryPi_IP = '127.0.0.1'
#        self.Laptop_IP = '127.0.0.1' # sink ( Laptop's address )

        self.Port = 9005
        self.Autonomus_Port = 9000
        self.stream_Ports = ['5022','5000','10000']
        self.UDP_IP = self.Laptop_IP
        self.UDP_Port = 8005
        self.Hat_address = 0x40
        self.Motors_Frequency = 50
        self.Zero_Vertical = 400
        self.Qt_String = {'x':0,'y':100,'r':0,'z':0,'cam':0}
        self.hat_delay = 0.000020 # us
        self.sample_time = 0.015

        self.pipeline1 = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=" + self.Laptop_IP + " port=" + self.stream_Ports[0] 
        self.pipeline2 = "v4l2src device=/dev/video1 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=" + self.Laptop_IP + " port=" + self.stream_Ports[2] 
        self.pipeline3 = "v4l2src device=/dev/video2 ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=10.1.1.14 port=1234"
        # for Laptop's Camera
#        self.pipeline1 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5022 sync=false"
#        self.pipeline2 = "v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! multiudpsink clients=127.0.0.1:1234,127.0.0.1:5022"

        # Qt String .. x=0,y=100,r=0,z=0,cam=0&
        # ========================================================

        self.selector =selectors.DefaultSelector()

        self.tcp_server = TCP(self.selector,self.RaspberryPi_IP, self.Port, self.Laptop_IP )

        self.observer_pattern = Observer_Pattern()
        self.hat = Hat( self.Hat_address, self.Motors_Frequency,self.hat_delay)
        self.motion = Motion(self.Qt_String)
        self.udp_client = UDP(self.UDP_IP ,self.UDP_Port)
        self.pid = PID(self.observer_pattern.emit_Signal)

        self.timer = Timer(1)
        self.Camera = Gstreamer(self.pipeline1)
        self.Camera2 = Gstreamer(self.pipeline2)
        self.Camera3 =Gstreamer(self.pipeline3)

        self.Camera.start()
        self.Camera2.start()

        self.hat.add_Device('Left_Front', 5, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Front', 2, self.motion.Zero_thruster)
        self.hat.add_Device('Right_Back', 13,self.motion.Zero_thruster)
        self.hat.add_Device('Left_Back',15 , self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Right', 9, self.motion.Zero_thruster)
        self.hat.add_Device('Vertical_Left', 11, self.motion.Zero_thruster)
        self.hat.add_Device('Main_Cam',0,self.motion.Zero_Servo)
        self.hat.add_Device('Back_Cam',1,self.motion.Zero_Servo)
        self.hat.add_Device('Magazine_Servo',3,self.motion.Zero_Magazie)
        self.hat.Raspberry_pi_Power(7,305)

        self.motion.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.tcp_server.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.hat.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        self.pid.SIGNAL_Referance(self.observer_pattern.emit_Signal)
        # Main Events
        self.observer_pattern.registerEventListener('HAT', self.hat.update)
        self.observer_pattern.registerEventListener('TCP', self.motion.update)
        self.observer_pattern.registerEventListener('TCP_ERROR', self.motion.update)
        # PID Integration Events
        self.observer_pattern.registerEventListener('PID',self.hat.update)
        self.observer_pattern.registerEventListener('SetPoint',self.pid.set_Setpoint_to_depth)
        self.observer_pattern.registerEventListener('ENABLE_PID',self.hat.Enable_PID)
        self.observer_pattern.registerEventListener('ENABLE_PID',self.pid.Enable_PID)
        self.observer_pattern.registerEventListener('Pilot_Enable',self.hat.Pilot_Enable)
        self.observer_pattern.registerEventListener('Pilot_Enable',self.pid.Pilot_Enable)
        # Buttons Events
        self.observer_pattern.registerEventListener('Temp',self.pid.get_Temp)
        self.observer_pattern.registerEventListener('Send_Temp',self.tcp_server.send_Temp)
        self.observer_pattern.registerEventListener('Micro_ROV',self.hat.update)
        self.observer_pattern.registerEventListener('Pulley',self.hat.update)

        self.observer_pattern.registerEventListener('Clean_GPIO',self.hat.update)

        self.main_Loop()

    def selector_print(self):
        conn = self.tcp_server.get_conn()
        sock = self.tcp_server.get_socket()
        if conn != None :
            print(self.selector.get_key(conn)[3],end=" $ ")
        if sock != None:
            print(self.selector.get_key(sock)[3])


    def main_Loop(self):
        print('Wait for zeft Qt')
        while True:
            try:
                events = self.selector.select(timeout=self.sample_time)

#                self.selector_print()
                for key, mask in events:
                    key.data()

                self.pid.Control_PID()

            except (TimeoutError,ConnectionResetError) :
                self.tcp_server.hard_Shutdown_Recreate_Socket()
            except KeyboardInterrupt:
                print(' Tari2 El Salama Enta')
                self.tcp_server.close()
                self.selector.close()
                self.Camera.close()
                self.Camera2.close()
                return

            # Important
            except:
                print("Exception Msh Ray2:",sys.exc_info()[0])
                self.tcp_server.hard_Shutdown_Recreate_Socket()

ORCA = ROV_19()
