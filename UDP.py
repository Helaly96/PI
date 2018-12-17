import socket
class UDP:
    def __init__(self,targetIp,port):
        self._targetIp=targetIp
        self._port=port
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def update(self,event,pressure,z):
        if event == 'CSV':
            message=(str(pressure)+" "+str(z)).encode(encoding="UTF-8")
            self.socket.sendto(message,(self._targetIp,self._port))

