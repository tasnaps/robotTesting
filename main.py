#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor
from pybricks.nxtdevices import LightSensor
import math as math
import time
ev3 = EV3Brick()

# Wheels on b and c for correct lego calibration
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# set third argument according to robot
# 170 for small wheel robot
#55,  120 for big wheel robot
base = DriveBase(left_motor, right_motor, 60, 170)
left_ir_sensor = Ev3devSensor(Port.S1)
right_ir_sensor = Ev3devSensor(Port.S2)
# when we set the robot in arena, must face forward we update heading in degrees turned
global heading
global rotation
global degreesToLine
global locationToLine
global angle

heading = 0
degreesToLine = 0
locationToLine = 0
angle = 0
rotation = 0



def deduct(value):
    if value > 1:
        value -= 1
        deduct(value)
    if value < -1:
        value +=1
        deduct(value)
    return value


def getRotation():
    global heading
    newHeading = heading/360
    newRotation = deduct(newHeading)
    #return angle in decimals
    return newHeading

def updateLocation():
    global locationToLine
    angle = getRotation()
    alpha = 180 - ((90)+angle*360)
    print(alpha)
    radians = math.radians(alpha)
    b = math.cos(radians) * 150
    print("b =: " + str(b))
    #positive = right side of the arena
    if (angle < 0.5 and angle >0.0):
        locationToLine = b + locationToLine
    if (angle >-1.0 and angle<-0.5):
        locationToLine = b + locationToLine

    #negative = left side of the arena
    if(angle<1 and angle >0.5):
        locationToLine = b + locationToLine
    if(angle<0 and angle>-0.5):
        locationToLine = b + locationToLine
    print("location to line: " + str(locationToLine))

def moveToLine():
    global rotation
    global degreesToLine
    tempHeading = getRotation() #value from -1 to 1
    if (tempHeading < 0):
        rotation = 1 - abs(tempHeading)
    else:
        rotation = 1 + tempHeading

    degreesToLine = (360 * rotation)-360    

    if locationToLine < 0:
        print("we are on the left side")
        if(degreesToLine<0):
            turn = abs(degreesToLine)
            time.sleep(1) 
            base.turn(turn + 90)
        if(degreesToLine>0):
            ev3.speaker.beep()
            time.sleep(3)
            turn = -degreesToLine
            base.turn(turn + 90)
            time.sleep(3)
        readAndMove()
        base.straight(30)
        base.turn(-90)
        ballControl = checkBallControl()
        if (ballControl):
            base.straight(500)
        else:
            movement()

    if locationToLine > 0:
        print("We are on the right side of the area")
        if(degreesToLine<0):
            base.turn(degreesToLine - 90)
        if(degreesToLine>0):
            degreesToLine = -degreesToLine - 90
            ev3.speaker.beep()
            time.sleep(1)
            base.turn(20)
            base.turn(-20)
            base.turn(degreesToLine)
            time.sleep(1)
        readAndMove()
        time.sleep(0.1)
        base.straight(20)
        base.turn(90)
        ballControl = checkBallControl()
        if (ballControl):
            ev3.speaker.beep()
            base.straight(500)
        else:
            movement()

def checkBallControl():
    left = left_ir_sensor.read("DC")
    right = right_ir_sensor.read("DC")
    if left[0] > 7 and right[0] < 4:
        # we still have the ball
        return True
    else:
        return False

def readAndMove():
    #left color sensor
    color_sensor = ColorSensor(Port.S3)
    color_sensor_value = color_sensor.reflection()
    ballControl = checkBallControl()
    time.sleep(0.5)
    if (ballControl):
        base.straight(abs(locationToLine))


def movement():
    left_ir_sensor_value = left_ir_sensor.read("DC")
    right_ir_sensor_value = right_ir_sensor.read("DC")
    global heading

    # ball is behind the robot
    if (right_ir_sensor_value[0] == 0 and left_ir_sensor_value[0] == 0):
        base.turn(40)
        heading += 40
        movement()

    # ball is to the right
    if right_ir_sensor_value[0] > 5:  # 60
        base.turn(20)
        heading += 20
        movement()

    # ball is to the left
    if left_ir_sensor_value[0] < 5:  # 4
        base.turn(-25)
        heading -= 25
        movement()

    # ball between sensors
    if left_ir_sensor_value[0] > 7 and right_ir_sensor_value[0] < 4:
        moveToLine()

    else:
        base.straight(150)
        updateLocation()
        movement()
movement()