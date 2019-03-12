from __future__ import division
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

while True:

    x = input("enter PWM:")
    x=int(x)
    pwm.set_pwm(3, 0, x)

