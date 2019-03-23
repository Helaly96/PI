from __future__ import division
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
y=input("enter channel: ")
y=int(y)
while True:

    x = input("enter PWM:")
    x=int(x)
<<<<<<< HEAD
    pwm.set_pwm(y, 0, x)
#    pwm.set_pwm(7, 0, x)
#    pwm.set_pwm(9, 0, x)
#    pwm.set_pwm(11, 0, x)
#    pwm.set_pwm(13, 0, x)
#    pwm.set_pwm(15, 0, x)

=======
    pwm.set_pwm(5, 0, x)
>>>>>>> 59b1c919f6b381d29c4324b6c6de23b7d243e48f

