import threading
import time
import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


class VideoStream():
    def __init__(self, pipeline):
        Gst.init(None)
        self._pipeline = Gst.parse_launch(pipeline)
            # "v4l2src device=/dev/video0 ! image/jpeg, width=1280, height=720, framerate=60/1 ! rtpjpegpay ! udpsink host=" + self._ip + " port=" + self._port + "sync=false")
        self._thread = None

    def start(self):
        ret = self._pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            raise Exception("Error starting the pipeline")

    def pause(self):
        self._pipeline.set_state(Gst.State.PAUSED)

    def close(self):
        self._running = False
        self._pipeline.set_state(Gst.State.NULL)
