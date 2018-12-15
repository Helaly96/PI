import socket
class UDP:
    def __init__(self,targetIp,port):
        self._targetIp=targetIp
        self._port=port
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def update(self,event,message):
        if event == 'SENSOR':
            message=str(message).encode(encoding="UTF-8")
            self.socket.sendto(message,(self._targetIp,self._port))

