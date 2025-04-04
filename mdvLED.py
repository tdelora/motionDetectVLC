"""
This Raspberry Pi code was developed with assistence from newbiely.com
newbiely.com Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-led-rgb

Thank you newbiely.com
"""

import RPi.GPIO as GPIO
from time import sleep
import mdvUtils


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def setColor(r,g,b):
    RED.ChangeDutyCycle(_map(r, 0, 255, 0, 100))
    GREEN.ChangeDutyCycle(_map(g, 0, 255, 0, 100))
    BLUE.ChangeDutyCycle(_map(b, 0, 255, 0, 100))
