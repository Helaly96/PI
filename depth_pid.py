import time
import sys
import ms5837
import Adafruit_PCA9685

p = 250
i = 53
d = 35

sample_time = 0.01  # seconds
depth = 0.0
setpoint = 0.7
sensor_offset = 0.0 # meter

sensor = ms5837.MS5837_30BA()
sensor.setFluidDensity(1000) # kg/m^3

pwm_zero = 305

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
pwm.set_pwm(8, 0, pwm_zero)
pwm.set_pwm(10, 0, pwm_zero)
pwm.set_pwm(3, 0, pwm_zero)

if not sensor.init():
        exit(1)
if not sensor.read():
    exit(1)

class PID:
    """PID Controller
    """

    def __init__(self, P, I, D):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.005
        self.current_time = time.time()
        self.last_time = self.current_time

        self.out_max = 400
        self.out_min = 260
        self.zero_offset = 305
        self.fwd_zero_offset = 317
        self.bwd_zero_offset = 296

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, set_point, feedback_value):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \ int_{0}^{t} e(t)dt + K_d {de}/{dt}

        """
        self.SetPoint = set_point
        error = self.SetPoint - feedback_value

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

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time

def calibrate_sensor(zero_reading):
	sensor_offset = zero_reading

if __name__ == '__main__':

    first_time_flag = 1

    setpoint = input("set point: ")
    setpoint = float(setpoint)
#    setpoint = 0.7

#    p = input("p: ")
#    p = float(p)

#    i = input("i: ")
#    i = float(i)

#    d = input("d: ")
#    d = float(d)

    depth_pid = PID(p, i, d)

    # print(depth_pid.output)

    try:
        while True:
            if sensor.read():
                depth = sensor.depth()

                if first_time_flag:
                    calibrate_sensor(float(depth))
                    first_time_flag = 0

                depth = float(depth) - sensor_offset

                print("Depth: %.3f m" % (depth))

                depth_pid.update(setpoint, depth)

                print("pwm: " + str(depth_pid.output))

                pwm.set_pwm(8, 0, depth_pid.output)
                pwm.set_pwm(10, 0, depth_pid.output)

            else :
                print("\n")

            time.sleep(sample_time)

    except KeyboardInterrupt:
        pwm.set_pwm(8, 0, pwm_zero)
        pwm.set_pwm(10, 0, pwm_zerp)
