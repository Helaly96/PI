import math

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

Neutral = 290
Brake = 140
Forward = 440
Joystick_min = -100
Joystick_max = 100


# 1 Up Left ... 2 Up Right ... # 3 Down Right ... # 4 Down Left
def Motion_Equation(x,y,r,z):

    pwm =[z,0,0,0,0]

    PureRotation = 0
    R14 =1
    R23 =1

    if r != 0:
        # to Make the Radius of Circle from the instantaneous centre of rotation is 2 * ROV Width
        # But it depends on Experiment .. and we can change that factor
        amount_of_Rotation = map(abs(r),0,Joystick_max,1,2/3)
        if x == 0 and y == 0:
            PureRotation = r
        elif y>0 and x ==0:
            if r > 0:
                R23 = amount_of_Rotation
            else:
                R14 = amount_of_Rotation

        elif y<0 and x ==0:
            if r > 0:
                R14 = amount_of_Rotation
            else:
                R23 = amount_of_Rotation


    # Convert to Circle Coordinates to limit the maximum speed
    # ================================================
    # The Circle Coordination support [-1,1] range
    x = map(x,Joystick_min,Joystick_max,-1,1)
    y = map(y,Joystick_min,Joystick_max,-1,1)

    Xc = x*math.sqrt(1-y*y/2)
    Yc = y*math.sqrt(1-x*x/2)

    Xc = map(Xc,-1,1,Joystick_min,Joystick_max)
    Yc = map(Yc,-1,1,Joystick_min,Joystick_max)
    #================================================

    # Axis Rotation
    X = Xc*math.cos(math.pi/4)+Yc*math.sin(math.pi/4)
    Y = -Xc*math.sin(math.pi/4)+Yc*math.cos(math.pi/4)

    R = math.sqrt(X*X+Y*Y)
    theta = math.atan2(Y,X)

    coff=1

    # in this durations tan theta is < 1 but > sin (the same theta)
    if ( theta >= -math.pi/4 and theta <= math.pi/4 ) or ( theta > -math.pi and theta <= -3*math.pi/4 ) or ( theta > 3*math.pi/4 and theta <= math.pi) :
        coff = abs(math.cos(theta))
    # in this durations tan theta is > 1 then cot theta < 1
    elif (theta > math.pi/4 and theta <= 3*math.pi/4) or (theta > -3*math.pi/4 and theta < -math.pi/4) :
        coff = abs(math.sin(theta))

    Motor1 =( (R*math.cos(theta) / coff) +PureRotation )*R14
    Motor2= ( (R*math.sin(theta) / coff) -PureRotation )*R23
    Motor3= ( (R*math.cos(theta) / coff) -PureRotation )*R23
    Motor4= ( (R*math.sin(theta) / coff) +PureRotation )*R14

    # Convert Joystick Coordinates to PWM
    pwm[1] = map(Motor1,Joystick_min,Joystick_max,Brake,Forward)
    pwm[2] = map(Motor2,Joystick_min,Joystick_max,Brake,Forward)
    pwm[3] = map(Motor3,Joystick_min,Joystick_max,Brake,Forward)
    pwm[4] = map(Motor4,Joystick_min,Joystick_max,Brake,Forward)
    pwm[0] = map(pwm[0],Joystick_min,Joystick_max,Brake,Forward)

    print (pwm)
Motion_Equation(0,-100,0,0)
