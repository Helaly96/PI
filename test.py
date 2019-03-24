from VideoStream import *
cam = Gstreamer("v4l2src device=/dev/video1 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=10.1.1.14 port=5022")
import time
while True:
     time.sleep(1)
