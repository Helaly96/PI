from __future__ import division
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:

    x = input("enter PWM:")
    x=int(x)
    pwm.set_pwm(4, 0, x)
    pwm.set_pwm(7, 0, x)
    pwm.set_pwm(8, 0 ,x)
    pwm.set_pwm(11, 0, x)
    pwm.set_pwm(12,0, x)
    pwm.set_pwm(15,0, x)
