import selectors
import socket
import sys
import subprocess
import time
class TCP :
    def __init__(self,selector,ip:str,port:int, streamingIP:str ,stream_ports:list):
        self._buffer_size = 1024
        self.Num_Of_tokens = 6
        self._ip = ip
        self._port = port
        self._streamIP = streamingIP
        self._streaming_ports = stream_ports.copy()
        self._conn = None
        self._client_address = None
        self._emit_Signal = None
        self._stream_disconect = False
        self.Connected = True
        self.false = 0 
        self.file = open("file.txt",'w')

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
            print("sh5al 5las")
#            self._port = int(input('port: '))
#            self._bind_Listen()
            quit()
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

    def _recv(self):
        data = self._conn.recv(self._buffer_size).decode(encoding="UTF-8")

        if not data: # disconnection return empty string ""
            self._stream_disconect = True
            self.close()
            return

        Qt_string = str()
        try:
            Qt_string = self.Split_to_Dict(data)
        except Exception as e:
            print(e,'wrong msg in recv')
            return
        if Qt_string == None:
            return

        if self._emit_Signal is None:
            print("emit signal dose not exist")
            return

        self._emit_Signal("TCP",Qt_string)

    def close(self):
        self._emit_Signal('TCP_ERROR',{})
        if self._conn is not None:
            self._selector.unregister(self._conn)
            self._conn.close()
        self._conn = None

    def Split_to_Dict(self,qt_string: str):
        tokens = qt_string.split(',')
        # delete the last element (it is empty)
        del tokens[len(tokens) - 1]
        Qt_string = {}
        count = self.Num_Of_tokens
        if len(tokens) > count:
            tokens_clone = tokens
            tokens = [""] * count
            try:
                for i in range(count):
                    tokens[i] = tokens_clone[(len(tokens_clone) - count) + i]
            except IndexError:
                print("Rubbish Qt string")
        elif len(tokens) < count:
            print('num of tokens error')
            return None

        for term in tokens:
            temp_list = term.split("=")
            Qt_string[temp_list[0]] = int(temp_list[1])

        return Qt_string

    def update(self,event,pressure):
        if self._conn != None or self.false:
            self.false = 1 
            addr = "1.1.1.2"
            response = subprocess.call(['ping','-c','3',addr])
            self.file.write(str(response)+'\n')
            if response != 0 :
                self._emit_Signal('TCP_ERROR',{})
                time.sleep(1)
                print("el socket maat")
                return 

#            self._conn.send((str(pressure)).encode())

