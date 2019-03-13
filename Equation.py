import time
import math
class Motion:
    def __init__(self,Qt_String):

        self.emit_signal = None
        self._Qt_String = Qt_String.copy()
        # =========== Constants ===========
        self.Zero_thruster = 305
        self.Zero_Servo = 225
        self.Servo_min = 150
        self.Servo_max = 570
        self.Brake = 240
        self.Forward = 420
        self.Joystick_min = -100
        self.Joystick_max = 100
        self.Rotation_Efficiency = 0.20
        self.Rotation_Speed = 0.40
        self.PWM_Map_Coff = (1 / self.Joystick_max) * (self.Forward - self.Zero_thruster)
        self.PWM_Map_Coff_reverse = (1 / self.Joystick_max) * (self.Zero_thruster-self.Brake)
        self.Zero_Magazie = 350
        self.CoffZ_reverse = 0.5
        self.CoffZ = 0.9
        self.camera_step = 5
        self.delay = False
        # =========== Motors==============
        self._horizontalMotors= {}
        self._verticalMotors  = {}
        self._servos =  {}
        self._lights =  {}
        # ======= initialization ===========
        self._stopHorizontalMotors()
        self._stopVerticalMotors()
        self._setCamToNormalPosition()
        self._turnLightOff()
        # ==================================
    def setRangeZ(self,x):
        if x == 0 :
            self.CoffZ = 0.7
        elif x ==1 :
            self.CoffZ = 1
    def _stopHorizontalMotors(self):
        self._horizontalMotors['Left_Front'] = self.Zero_thruster
        self._horizontalMotors['Right_Front'] = self.Zero_thruster
        self._horizontalMotors['Right_Back'] = self.Zero_thruster
        self._horizontalMotors['Left_Back'] = self.Zero_thruster
    def _stopVerticalMotors(self):
        self._verticalMotors['Vertical_Right'] = 400
        self._verticalMotors['Vertical_Left'] = 400
    def _setCamToNormalPosition(self):
        self._servos['Main_Cam'] = self.Zero_Servo
        self._servos['Back_Cam'] = self.Zero_Servo
        self._servos['Magazine_Servo'] = 1450
    def _turnLightOff(self):
        self._lights['light'] = 0
    def Map (self,x,motor):
        if x <= 0 :
            return self.Zero_thruster + x * self.PWM_Map_Coff_reverse
        elif motor == "Left_Front" :
            return self.Zero_thruster + x * self.PWM_Map_Coff
        elif motor == "Right_Front" :
            return self.Zero_thruster + x * self.PWM_Map_Coff * 0.7
        elif motor == "Right_Back" :
            return self.Zero_thruster + x * self.PWM_Map_Coff * 0.8
        elif motor == "Left_Back" :
            return self.Zero_thruster + x * self.PWM_Map_Coff
    @staticmethod
    def map(value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)
    def calculateHorizontalMotors_19(self):
        x =self._Qt_String['x']
        y =self._Qt_String['y']
        r =self._Qt_String['r']

        theta = math.atan2(y, x)

        # ============== Skip ============================
        # Check https://ibb.co/ir10AV
        # R = math.hypot(x, y) * (max(abs(math.sin(theta)), abs(math.cos(theta))))
        # ================================================

        # Convert to Circle Coordinates to limit the maximum speed
        # Check https://www.xarg.org/2017/07/how-to-map-a-square-to-a-circle/
        # ================================================
        # The Circle Coordination Equation support [-1,1] range
        X = x / self.Joystick_max
        Y = y / self.Joystick_max

        Xc_2 = X * X * (1 - Y * Y / 2)
        Yc_2 = Y * Y * (1 - X * X / 2)

        R = math.sqrt(Xc_2 + Yc_2) * self.Joystick_max
        # ================================================
        # Axis Rotation
        theta -= math.pi / 4
        # Coefficient to Get the Best Speed of Motors
        # Check https://ibb.co/fYUZ4q   # Check https://ibb.co/dSFqPf
        coff = max(abs(math.sin(theta)), abs(math.cos(theta)))
        # ============ ( C ) is Rotation Efficiency =================
        C = self.map(abs(r),0,self.Joystick_max,0,self.Rotation_Efficiency)
        # C = self.Rotation_Efficien
        if R == 0 :
            C = self.Rotation_Speed
        # ===========================================================

        R_Cos_Coff = R * math.cos(theta) / coff
        R_Sin_Coff = R * math.sin(theta) / coff

        Motor1 = (1-C) * R_Cos_Coff + C *r
        Motor2 = (1-C) * R_Sin_Coff - C *r
        Motor3 = (1-C) * R_Cos_Coff - C *r
        Motor4 = (1-C) * R_Sin_Coff + C *r


        # Map the Joystick Coordinates to PWM Coordinates

        self._horizontalMotors['Left_Front']  = int(self.Map(Motor1,'Left_Front') )
        self._horizontalMotors['Right_Front'] = int(self.Map(Motor2,'Right_Front') )
        self._horizontalMotors['Right_Back']  = int(self.Map(Motor3,'Right_Back') )
        self._horizontalMotors['Left_Back']  = int(self.Map(Motor4,'Left_Back') )

        # print(pwm)
    def calculateVerticalMotors_19(self):
        # steps = real pwm range / freq  = 250 M / 50 = 5 M (5000000)
        # z = Motion.map (self._Qt_String['z'] , self.Joystick_min,self.Joystick_max,300,500)
        Z = self._Qt_String['z']
        if Z >= 0:
            z = self.Zero_thruster + Z * self.CoffZ
        elif Z < 0 :
            z = self.Zero_thruster + Z * self.CoffZ_reverse

        self._verticalMotors['Vertical_Right'] = int(z)
        self._verticalMotors['Vertical_Left'] =  int(z)

    def moveCamera(self):
        if self._Qt_String['cam'] == 1 and self._servos['Main_Cam'] > self.Servo_min  :
            self._servos['Main_Cam'] -= self.camera_step
            self._servos['Back_Cam'] -= self.camera_step
        elif self._Qt_String['cam'] == 4 and self._servos['Main_Cam'] < self.Servo_max:
            self._servos['Main_Cam'] += self.camera_step
            self._servos['Back_Cam'] += self.camera_step
        elif self._Qt_String['cam'] == 2:
            self._servos['Magazine_Servo'] = 100
        elif self._Qt_String['cam'] == 8:
            self._servos['Magazine_Servo'] = 700
 

    def light(self):
        if self._lights['light'] < 1800:
            self._lights['light'] += 500
        else:
            self._lights['light'] = 0

    def SIGNAL_Referance(self,Observer_Pattern_Signal):
        self.emit_signal=Observer_Pattern_Signal
    def print_PWM(self):
        print(self._horizontalMotors,self._verticalMotors)

    def update(self,event_name,Qt_String):


        if event_name == 'TCP_ERROR' :
            self._stopVerticalMotors()
            self._stopHorizontalMotors()
            self._setCamToNormalPosition()
            self._turnLightOff()
            print('TCP_ERROR 8adaro beena')

        elif event_name == 'TCP':
            self._Qt_String = Qt_String.copy()
            self.calculateVerticalMotors_19()
            self.calculateHorizontalMotors_19()

            if self._Qt_String['cam'] != 0:
                 self.moveCamera()
                 self.delay = True
            else :
                 self._servos['Magazine_Servo'] = self.Zero_Magazie
            if self._Qt_String['light'] !=0:
                 self.light()

#            if self._Qt_String['z'] !=0:
#                self._stopHorizontalMotors()
#                self.calculateVerticalMotors_19()
#            else:
#                self._stopVerticalMotors()
#                self.calculateHorizontalMotors_19()

        pwm = {}
        pwm.update(self._horizontalMotors)
        pwm.update(self._verticalMotors)
        pwm.update(self._servos)

        self.emit_signal('HAT',pwm)
        if self.delay :
            time.sleep(0.1) 
        self.delay = False
        self.print_PWM()

