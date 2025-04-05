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

class ledStatusClass:
	def __init__(self):
		self.showLED = False
		self.redPin = 13
		# self.greenPin = 12
		self.greenPin = 6
		self.bluePin = 18

		GPIO.setmode(GPIO.BCM)
		GPIO.setup([self.redPin, self.greenPin, self.bluePin],GPIO.OUT)
		self.RED = GPIO.PWM(self.redPin, 1000)
		self.GREEN = GPIO.PWM(self.greenPin, 1000)
		self.BLUE = GPIO.PWM(self.bluePin, 1000)

	def _duty(self,x, in_min, in_max, out_min, out_max):
    		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	def setColor(self,redVal,greenVal,blueVal):
		print(f"mdvLED.setColor: r:{redVal} g:{greenVal} b:{blueVal}")
		self.RED.ChangeDutyCycle(self._duty(redVal, 0, 255, 0, 100))
		self.GREEN.ChangeDutyCycle(self._duty(greenVal, 0, 255, 0, 100))
		self.BLUE.ChangeDutyCycle(self._duty(blueVal, 0, 255, 0, 100))

	def start(self,showLED):
		self.showLED = showLED

		if self.showLED:
			self.RED.start(0)
			self.GREEN.start(0)
			self.BLUE.start(0)


	def stop(self):
		if self.showLED:
			self.RED.stop()
			self.GREEN.stop()
			self.BLUE.stop()
			GPIO.cleanup()
