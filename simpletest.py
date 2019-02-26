# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:

    x = input("enter PWM:")
    x=int(x)
#    pwm.set_pwm(4, 0, x)
#    pwm.set_pwm(7, 0, x)
#    pwm.set_pwm(8, 0 ,x)
#    pwm.set_pwm(11, 0, x)
    pwm.set_pwm(12,0, x)
#  pwm.set_pwm(15,0, x)
