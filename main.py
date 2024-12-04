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
    while value > 1:
        value -= 1
    while value < -1:
        value += 1
    return value

def getRotation():
    global heading
    newHeading = heading / 360
    newRotation = newHeading % 1
    return newRotation

def updateLocation():
    global locationToLine
    angle = getRotation()
    alpha = 180 - (90 + angle * 360)
    radians = math.radians(alpha)
    b = math.cos(radians) * 150
    locationToLine += b
    print("location to line: " + str(locationToLine))

def moveToLine():
    global rotation
    global degreesToLine
    tempHeading = getRotation()
    rotation = 1 + tempHeading if tempHeading >= 0 else 1 - abs(tempHeading)
    degreesToLine = (360 * rotation) - 360

    if locationToLine < 0:
        print("we are on the left side")
        turn = abs(degreesToLine) if degreesToLine < 0 else -degreesToLine
        base.turn(turn + 90)
        readAndMove()
        base.straight(30)
        base.turn(-90)
        if checkBallControl():
            base.straight(500)
        else:
            movement()
    else:
        print("We are on the right side of the area")
        turn = degreesToLine - 90 if degreesToLine < 0 else -degreesToLine - 90
        base.turn(turn)
        readAndMove()
        base.straight(20)
        base.turn(90)
        if checkBallControl():
            base.straight(500)
        else:
            movement()

def checkBallControl():
    left = left_ir_sensor.read("DC")
    right = right_ir_sensor.read("DC")
    return left[0] > 7 and right[0] < 4

def readAndMove():
    color_sensor = ColorSensor(Port.S3)
    color_sensor_value = color_sensor.reflection()
    if checkBallControl():
        base.straight(abs(locationToLine))

def movement():
    left_ir_sensor_value = left_ir_sensor.read("DC")
    right_ir_sensor_value = right_ir_sensor.read("DC")
    global heading

    if right_ir_sensor_value[0] == 0 and left_ir_sensor_value[0] == 0:
        base.turn(40)
        heading += 40
    elif right_ir_sensor_value[0] > 5:
        base.turn(20)
        heading += 20
    elif left_ir_sensor_value[0] < 5:
        base.turn(-25)
        heading -= 25
    elif left_ir_sensor_value[0] > 7 and right_ir_sensor_value[0] < 4:
        moveToLine()
    else:
        base.straight(150)
        updateLocation()
    movement()

movement()
