import selectors
import socket
import sys

class TCP :
    def __init__(self,selector,ip:str,port:int, streamingIP:str ,stream_ports:list):
        self._buffer_size = 1024
        self.Num_Of_tokens = 8
        self._ip = ip
        self._port = port
        self._streamIP = streamingIP
        self._streaming_ports = stream_ports.copy()
        self._conn = None
        self._client_address = None
        self._emit_Signal = None
        self._stream_disconect = False


        self._selector = selector
        self._create_Socket()
        self._bind_Listen()

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self._emit_Signal=Observer_Pattern_Signal

    def _create_Socket(self):
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _bind_Listen(self):
        try:
            self._socket.bind( (self._ip,self._port) )
            self._socket.listen(1)
        except socket.error:
            print('socket error while binding socket')
            self._port = int(input('port: '))
            self._bind_Listen()
            return

        self._socket.setblocking(False)
        self._selector.register(self._socket,selectors.EVENT_READ,self._acceept)

    def _acceept(self):
        # if someone tries to connect the pi while it is already connected
        if self._conn is not None:
            # to pull the event from selectors
            new_conn , new_addr = self._socket.accept()
            new_conn.close()
            print("something tries to connect to pi ")
            return
        # ===================== TCP Server ========================
        self._conn , self._client_address = self._socket.accept()
        print('Connected ya ray2      ',self._client_address)
        self._conn.setblocking(False)
        self._selector.register(self._conn,selectors.EVENT_READ,self._recv)
        # =========================================================

        #
        # # ==================== Gstreamer ==========================
        # import VideoStream
        # #self._pipeline1 = "v4l2src device=/dev/video0 ! image/jpeg, width=1280, height=720, framerate=60/1 ! rtpjpegpay ! multiudpsink clients=" + self._streamingIP + ":" + self._streaming_ports[0] + "," + self._streamingIP + ":" + s$
        # #self._videoStream = VideoStream.VideoStream(self._pipeline1)
        # #self._videoStream.start()
        # self._pipeline2 = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=" + self._streamIP + " port=" + self._streaming_ports[0]  # + " sync=false"
        # self._videoStream2 = VideoStream.VideoStream(self._pipeline2)
        # self._videoStream2.start()
        # # =========================================================
        # if self._stream_disconect:
        #     self._videoStream2.start()
        #     self._stream_disconect =False

    def _recv(self):
        data=str()
        try:
            data = self._conn.recv(self._buffer_size).decode(encoding="UTF-8")
        except socket.error:
            if not data:
                self._stream_disconect = True
                self._close()
                return

        Qt_string = str()
        try:
            Qt_string = self.Split_to_Dict(data)
        except Exception as e:
            print(e,'wrong msg in recv')
            return
        if self._emit_Signal is None:
            print("emit signal dose not exist")
            return

        self._emit_Signal("TCP",Qt_string)

    def _close(self):
        self._emit_Signal('TCP_ERROR',{})
        if self._conn is not None:
            self._selector.unregister(self._conn)
            self._conn.close()
        self._conn = None
#         if self._stream_disconect:
#     #       self._videoStream2.pause()
#
# #       self._videoStream2.close()


    def Split_to_Dict(self,qt_string: str):
        tokens = qt_string.split(',')
        # delete the last element (it is empty)
        del tokens[len(tokens) - 1]

        Qt_string = {}
        count = self.Num_Of_tokens
        if len(tokens) != count:
            tokens_clone = tokens
            tokens = [""] * count
            try:
                for i in range(count):
                    tokens[i] = tokens_clone[(len(tokens_clone) - count) + i]
            except IndexError:
                print("Rubbish Qt string")
        for term in tokens:
            temp_list = term.split('=')
            Qt_string[temp_list[0]] = int(temp_list[1])

        return Qt_string

    def main_Loop(self):
        print('Wait for zeft Qt')
        while True:
            try:
                events = self._selector.select()
                for key, mask in events:
                    key.data()
            except KeyboardInterrupt:
                print(' End')
                self._close()
                return


