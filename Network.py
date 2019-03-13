import selectors
import socket

class TCP :
    def __init__(self,selector,ip:str,port:int, streamingIP:str ,stream_ports:list):
        self._buffer_size = 1024
        self.Num_Of_tokens = 6
        self._ip = ip
        self._port = port
        self._streamIP = streamingIP
        self._streaming_ports = stream_ports.copy()
        self._socket = None
        self._conn = None
        self._client_address = None
        self._emit_Signal = None
        self._stream_disconect = False

        self._selector = selector
        self._create_Socket()
        self._bind_Listen()

        print(self._selector)
    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self._emit_Signal=Observer_Pattern_Signal

    def _create_Socket(self):
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)

    def get_socket(self):
        return self._socket
    def get_conn(self):
        return self._conn
    def _bind_Listen(self):
        try:
            self._socket.bind( (self._ip,self._port) )
            self._socket.listen(1)
        except socket.error:
            print('socket error while binding socket')
            print("sh5al 5las")
            quit()
            return

        self._socket.setblocking(False)
        self._selector.register(self._socket,selectors.EVENT_READ,self._acceept)

    def _acceept(self):
        # if someone tries to connect the pi while it is already connected
        if self._conn is not None:
            print("someone tries to connect pi")

            # ========== Close The old and open new Connection ===============================
            # self.close()
            # self._conn , self._client_address = self._socket.accept()
            # self._selector.register(self._conn,selectors.EVENT_READ,self._recv)
            # print("D5ool Rayaaaaaaaaaaaaaaaaaa2")

            # =========== Pull the Event from Selectors and close it and keep the old =========
            temp_conn , _ = self._socket.accept()
            temp_conn.close()
            return
        # ===================== TCP Server ========================
        self._conn , self._client_address = self._socket.accept()
        print('Connected ya ray2      ',self._client_address)

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)

        self._conn.setblocking(False)
        self._selector.register(self._conn,selectors.EVENT_READ,self._recv)
        # =========================================================

    def _recv(self):
        data = self._conn.recv(self._buffer_size).decode(encoding="UTF-8")
#        print(data)
        if not data: # disconnection return empty string ""
            self._stream_disconect = True
            self.close()
            return
        try:
            Qtstrings=self.Split_to_Dict(data)
        except:
            print("Msg 8areeebaa Moreebaaaa 3ageeebaa")
            return
#        print(Qtstrings) 
        if Qtstrings == None:
            return

        for string in Qtstrings :
            self._emit_Signal("TCP",string)

    def close(self):
        self._emit_Signal('TCP_ERROR',{})
        if self._conn is not None:
            self._selector.unregister(self._conn)
            self._conn.close()
            self._conn = None

    def Split_to_Dict(self,qt_string: str):
        Qt_strings = []
        count = self.Num_Of_tokens


        msgs = qt_string.split('&')
        n = len (msgs)
        del msgs[ n -1 ]

        if n == 1:
            Qt_strings.append( {} )
            msg = msgs[0].split(',')
            for term in msg:
                temp_list = term.split("=")
                Qt_strings[0][temp_list[0]] = int(temp_list[1])
            return Qt_strings

        if n > 1 :
            for msg in msgs :
                temp_msg = msg.split(',')
                temp_Qt_string = {}
                for term in temp_msg:
                    temp_list = term.split("=")
                    temp_Qt_string[temp_list[0]] = int(temp_list[1])
                Qt_strings.append(temp_Qt_string)
#            print("Qt_strings:",Qt_strings)
            return Qt_strings

        elif n == 0:
            print('num of tokens error')
            return None

        return Qt_strings

    def hard_Shutdown_Recreate_Socket(self):
        self.close()
        self._selector.unregister(self._socket)
        self._socket.shutdown(2)
        self._socket.close()
        self._socket = None
        print("Socket is Dead Tari2 El Salama enta")
        self._create_Socket()
        self._bind_Listen()
        print("New Socket Created ...............")
