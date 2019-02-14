import time
import Adafruit_PCA9685

T = 0.2
Zero = 405
Point = {"PWM":Zero,"Thrust":0}

# ======= Adafruit Hat ===========
hat = Adafruit_PCA9685.PCA9685()
hat.set_pwm_freq(50)
channel = 0
hat.set_pwm(channel, 0, Zero)


# ====== Thrust Measurement =======
def update_thrust():
    thrust = 1
    return thrust

file = open("Motor", "w")

while Point["PWM"] <= 500 and Point["PWM"] >= 300 :

    Point["PWM"] = Point["PWM"] +1
    hat.set_pwm(channel , 0 , Point["PWM"] )
    # Wait for Motor Response
    time.sleep(T)

    Point["Thrust"] = update_thrust()

    data = str(Point["PWM"]) + ' ' + str(Point["Thrust"])

    file.write(data)
    file.write("\n")
    print(Point)


file.close()
hat.set_pwm(channel, 0, Zero)
print("Tari2 El Salama Enta")
