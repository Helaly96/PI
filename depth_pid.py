import time
import ms5837


class PID:
    """PID Controller
    """

    def __init__(self, emitsignal):
        self.emit_Signal =  emitsignal
        self.pilot_enable = False
        self.enable = False
# 250 53 35
        self.Kp = 250
        self.Ki = 53
        self.Kd = 35

        self.sensor = ms5837.MS5837_30BA()
        self.sensor.setFluidDensity(1000)  # kg/m^3

        self.sample_time = 0.01
        self.current_time = time.time()
        self.last_time = self.current_time

        self.SetPoint = 0.7
        self.depth = 0.0
        self.sensor_offset = 0.4
        self.pwm_zero = 305

#        self.sensor = SENSOR()

#        self.sensor.setFluidDensity(1000)  # kg/m^3

        self.out_max = 400
        self.out_min = 240
        self.zero_offset = 305
        self.fwd_zero_offset = 317
        self.bwd_zero_offset = 296

        if not self.sensor.init():
            exit(1)
        if not self.sensor.read():
            exit(1)


        self.clear()

    def clear(self):
#        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0
    def SIGNAL_Referance(self,emit_signal):
        self.emit_Signal=emit_signal

    def update(self, set_point, feedback_value):
        self.SetPoint = set_point
        error = self.SetPoint - feedback_value
#        print("Set Point: "+str(self.SetPoint))
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
#            print("output"+str(self.output))
            # add pwm zero offset to output
            self.output += self.zero_offset

            # account for min and max ranges
            if self.output > self.out_max:
                self.output = self.out_max
            elif self.output < self.out_min:
                self.output = self.out_min

            # account for dead zone
            if (self.output > self.zero_offset) and (self.output < self.fwd_zero_offset):
                self.output = self.fwd_zero_offset
            elif (self.output < self.zero_offset) and (self.output > self.bwd_zero_offset):
                self.output = self.bwd_zero_offset

        self.output = int(self.output)

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

    def calibrate_sensor(self,zero_reading):
        self.sensor_offset =  0



    def get_Temp(self,event):
        self.emit_Signal ('Send_Temp',self.sensor.temperature(ms5837.UNITS_Centigrade) )

    def set_Setpoint_to_depth(self,event_name,flag):
        if flag :
            self.SetPoint=self.sensor.depth()

    def Pilot_Enable(self,event,enable):
        self.pilot_enable = enable
        print("Pilot_Enable:", self.pilot_enable)

    def Enable_PID(self,event,enable):
        self.enable = enable

    def Control_PID(self,s):

        first_time_flag = 1
        try:
            while True:
                if self.pilot_enable and self.enable:
            # ==============================================================
                    if self.sensor.read():
                        self.depth = self.sensor.depth()

                        self.depth = float(self.depth) - self.sensor_offset
                        self.update(self.SetPoint, self.depth)

                        print("Depth: %.3f m" % (self.depth),"pwm: " + str(self.output))
                        self.emit_Signal("PID",self.output)
                    else :
                        print("Sensor read unavalable,\n")

                    time.sleep(0.005)
                # ==============================================================
                else:
    #                print ("Pilot_Enable:",self.pilot_enable)
                    time.sleep(0.5)
        except KeyboardInterrupt:
            self.emit_Signal("PID",self.pwm_zero)


# def ray2(event,output):
#     return
# pid = PID(ray2)
# pid.Control_PID(5)

