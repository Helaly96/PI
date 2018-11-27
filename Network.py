# Check https://pymotw.com/3/selectors/
# Check https://docs.python.org/3/library/selectors.html
import selectors
import socket

class TCP :
    def __init__(self,ip:str,port:int, streamingIP:int ,stream_ports:list):
        self._buffer_size = 1024
        self.Num_Of_tokens = 6
        self._ip = ip
        self._port = port
        self._streamIP = streamingIP
        self._streaming_ports = stream_ports.copy()
        self._conn = None
        self._client_address = None
        self._emit_Signal = None


        self._selector = selectors.DefaultSelector()
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
            self._ip = input('ip: ')
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

        self._conn , self._client_address = self._socket.accept()
        print('Connected ya ray2      ',self._client_address)

        self._conn.setblocking(False)
        self._selector.register(self._conn,selectors.EVENT_READ,self._recv) # Start listening for a msg just after accept (connecting with client)

    def _recv(self):
        data = str()
        try:
            data = self._conn.recv(self._buffer_size).decode(encoding="UTF-8")
        except :
            if not data:
                self._close()
                return

        Qt_string = self.Split_to_Dict(data)

        if self._emit_Signal is None:
            print("emit signal dose not exist")
            return

        self._emit_Signal("TCP",Qt_string)

    def _close(self):
        # self._emit_Signal('TCP_ERROR',{})
        if self._conn is not None:
            self._selector.unregister(self._conn)
            self._conn.close()
        self._conn = None


    def Split_to_Dict(self,qt_string: str):
        tokens = qt_string.split(';')
        # delete the last element (it is empty)
        del tokens[len(tokens) - 1]

        Qt_string = {}
        count = self.Num_Of_tokens
        if len(tokens) != count:
            tokens_clone = tokens
            tokens = [""] * count
            for i in range(count):
                tokens[i] = tokens_clone[(len(tokens_clone) - count) + i]
            print(tokens)

        for term in tokens:
            temp_list = term.split(':')
            Qt_string[temp_list[0]] = int(temp_list[1])

        print(Qt_string)
        return Qt_string

    def main_Loop(self):
        while True:
            events = self._selector.select()
            for key, mask in events:
              key.data()

TCP_OBJ = TCP('127.0.0.1',8082,1000000,[])
TCP_OBJ.main_Loop()

