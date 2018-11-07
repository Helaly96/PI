import socket
import Adafruit_PCA9685

Neutral = 290
Brake_Force = 140
Forward_Force = 440
# ============================== PWM ========================
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
# ===========================================================
class Hat:
    def __init__(self,Motors, Servoes = None):
        self.Motors = Motors
        self.Servos = Servoes

    def Move(self,pwms):
        for i, motor in enumerate(Motors):
            motor.Set_Speed(pwms[i])

# ===========================================================
#====================== Servo  =============================
servo_zero = 160
servo_90 = 370
servo_180 = 580

class servo:
        def __init__(self,pin):
                self.pin = pin
                self.pos = servo_90
                pwm.set_pwm(self.pin,0,self.pos)

        def Set_Servo_Pos(self,x):
                if x == 'u' and self.pos < servo_180:
                        self.pos += 21
                        pwm.set_pwm(self.pin,0,self.pos)
                elif x == 'd' and self.pos > servo_zero:
                        self.pos -= 21
                        pwm.set_pwm(self.pin,0,self.pos)

#===========================================================

class Motor:
        def __init__(self,pin_num):
                if pin_num >15 or pin_num <0:
                        print('error pin Num')
                        return
                self.__pin = pin_num
                self.__speed = 0

        def Set_Speed(self,speed):
                if speed == self.__speed :
                    return
                # check for joystick error
                if speed < Brake_Force or speed > Forward_Force:
                    print("PWM Range Error")
                    return
                pwm.set_pwm(self.__pin, 0, speed)
                self.__speed = speed

class Subject:
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    def subject_state(self):
        return self._subject_state

    def subject_state(self, arg):
        self._subject_state = arg
        self._notify()


class Observer:
    def __init__(self):
        self._subject = None
        self._observer_state = None
    def update(self, arg):
        pass


class Network(Observer):
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn, self.addr = self.s.accept()
        try:
            self.s.bind((host, port))
            print('Waiting for QT Connection!')
        except socket.error as m:
            print('Bind failed. Error Code : ' + str(m[0]))
        self.s.listen(5)
    def update(self, arg):
        pass


# Motors = []
# Motors.append(Motor(1))
# Motors.append(Motor(2))
# Motors.append(Motor(3))
# Motors.append(Motor(4))
# 
# Motors.append(Motor(13))
# Motors.append(Motor(14))
# 
# HAT = Hat(Motors)
