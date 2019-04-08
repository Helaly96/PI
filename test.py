from VideoStream import *
import time

cam = Gstreamer("v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5022")

while True:
     x = input("x: ")
     x = int(x)
     if x == 1 and not cam.running:
      cam.start()
     elif x == 0 and cam.running:
      cam.close()

     time.sleep(1)
