import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class Gstreamer():
    def __init__(self, pipeline):
        Gst.init(None)
        self._pipeline = Gst.parse_launch(pipeline)
            # "v4l2src device=/dev/video0 ! image/jpeg, width=1280, height=720, framerate=60/1 ! rtpjpegpay ! udpsink host=" + self._ip + " port=" + self._port + "sync=false")
    def start(self):
        try:
            ret = self._pipeline.set_state(Gst.State.PLAYING)
            if ret == Gst.StateChangeReturn.FAILURE:
                raise Exception("Error starting the pipeline")
        except :
            print("wasl el camera ya sa3eed")
            return

        print("start")
    def pause(self):
        self._pipeline.set_state(Gst.State.PAUSED)
        print("Pause Camera")
    def close(self):
        self._running = False
        self._pipeline.set_state(Gst.State.NULL)

#camera = Gstreamer("v4l2src ! video/x-raw,width=640,height=480 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5022")


