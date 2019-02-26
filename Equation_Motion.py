import math
class Motion:
    def __init__(self):

        self.emit_signal = None
        self._Qt_String = None
        # =========== Constants ===========
        self.Zero_thruster = 400
        self.Zero_Servo = 225
        self.Servo_min = 150
        self.Servo_max = 600
        self.Brake = 360
        self.Forward = 440
        self.Joystick_min = -100
        self.Joystick_max = 100
        self.Rotation_Efficiency = 0.231
        self.PWM_Map_Coff = (1 / self.Joystick_max) * (self.Forward - self.Zero_thruster)
        # =========== Motors ==============
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

    def _stopHorizontalMotors(self):
        self._horizontalMotors['Left_Front'] = self.Zero_thruster
        self._horizontalMotors['Right_Front'] = self.Zero_thruster
        self._horizontalMotors['Right_Back'] = self.Zero_thruster
        self._horizontalMotors['Left_Back'] = self.Zero_thruster
    def _stopVerticalMotors(self):
        self._verticalMotors['Vertical_Right'] = self.Zero_thruster
        self._verticalMotors['Vertical_Left'] = self.Zero_thruster
    def _setCamToNormalPosition(self):
        self._servos['Main_Cam'] = self.Zero_Servo
    def _turnLightOff(self):
        self._lights['light'] = 0

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
        # C = self.Rotation_Efficiency
        if R ==0:
            C = 1
        # ===========================================================

        R_Cos_Coff = R * math.cos(theta) / coff
        R_Sin_Coff = R * math.sin(theta) / coff

        Motor1 = (1-C) * R_Cos_Coff + C *r
        Motor2 = (1-C) * R_Sin_Coff - C *r
        Motor3 = (1-C) * R_Cos_Coff - C *r
        Motor4 = (1-C) * R_Sin_Coff + C *r


        # Map the Joystick Coordinates to PWM Coordinates

        self._horizontalMotors['Left_Front']  = int(self.Zero_thruster + Motor1 * self.PWM_Map_Coff)
        self._horizontalMotors['Right_Front'] = int(self.Zero_thruster + Motor2 * self.PWM_Map_Coff* 0.8)
        self._horizontalMotors['Right_Back']  = int(self.Zero_thruster + Motor3 * self.PWM_Map_Coff)
        self._horizontalMotors['Left_Back']  = int(self.Zero_thruster + Motor4 * self.PWM_Map_Coff)

        # print(pwm)
    def calculateVerticalMotors_19(self):
        # steps = real pwm range / freq  = 250 M / 50 = 5 M (5000000)
        z = Motion.map (self._Qt_String['z'] , self.Joystick_min,self.Joystick_max,300,500)
        self._verticalMotors['Vertical_Right'] = int(z)
        self._verticalMotors['Vertical_Left'] =  int(z)

    def moveCamera(self):
        if self._Qt_String['cam'] == 1 and self._servos['Main_Cam'] < self.Servo_max  :
            self._servos['Main_Cam'] += 10
        elif self._Qt_String['cam'] == 4 and self._servos['Main_Cam'] > self.Servo_min:
            self._servos['Main_Cam'] -= 10

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

            if self._Qt_String['z'] !=0:
                self._stopHorizontalMotors()
                self.calculateVerticalMotors_19()
            else:
                self._stopVerticalMotors()
                self.calculateHorizontalMotors_19()

#             if self._Qt_String['Cam_H_Servo'] != 0:
#                 self.moveCamera('Cam_H_Servo',self._Qt_String['Cam_H_Servo'])
#             if self._Qt_String['Cam_V_Servo'] != 0:
#                 self.moveCamera('Cam_V_Servo',self._Qt_String['Cam_V_Servo'])
#             if self._Qt_String['Back_Cam'] !=0 :
#                 self.moveCamera('Back_Cam',self._Qt_String['Back_Cam'])

            if self._Qt_String['cam'] != 0:
                 self.moveCamera()
            if self._Qt_String['light'] !=0:
                 self.light()

        pwm = {}
        pwm.update(self._horizontalMotors)
        pwm.update(self._verticalMotors)
        pwm.update(self._servos)
#        pwm.update(self._lights)

        print(pwm)
        self.emit_signal('HAT',pwm)
        self.print_PWM()
