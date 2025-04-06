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

	gpioPins = {'redPin':13,'greenPin':6,'bluePin':18}
	statusModes = {'start':"#FF0000",'bored':"#0000FF",'no_motion':"#ff8000",'motion':"#301934",'waiting':"#00FF00"}
	
	def __init__(self):
		self.showLED = False
		GPIO.setmode(GPIO.BCM)

	def _duty(self,x, in_min, in_max, out_min, out_max):
    		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	def setColor(self,hexString):
		if self.showLED:
			redVal, greenVal, blueVal = mdvUtils.colorHexTo8bit(hexString)
			# print(f"mdvLED.setColor: r:{redVal} g:{greenVal} b:{blueVal}")
			self.RED.ChangeDutyCycle(self._duty(redVal, 0, 255, 0, 100))
			self.GREEN.ChangeDutyCycle(self._duty(greenVal, 0, 255, 0, 100))
			self.BLUE.ChangeDutyCycle(self._duty(blueVal, 0, 255, 0, 100))

	def configure(self,ledConfig):
		returnValue = True

		if type(ledConfig) is dict:
			# Check for updates to gpioPins
			for key in gpioPins.keys():
				tmpPinInfo = mdvUtils.findKey(ledConfig,key)
				if tmpPinInfo != None:
					if mdvUtils.validateGPIOPin(key,tmpPinInfo):
						# A new pin number has been provided for this key
						gpioPin[key] = tmpPinInfos
					else:
						returnValue = False

			# Check for updates to statusModes
			for key in statusModes.keys():
				tmpHexString = mdvUtils.findKey(ledConfig,key)
				if tmpHexString != None:
					if mdvUtils.validateHexColor(tmpHexString):
						# A new color has been provided for this key
						statusModes[key] = tmpHexString
					else:
						returnValue = False

		elif ledConfig != None:
			print(f"mdvLED.configure: Received config info is not a dictionary")
			returnValue = False

		return returnValue

	def start(self,showLED):
		self.showLED = showLED

		if self.showLED:
			GPIO.setup([self.gpioPins["redPin"], self.gpioPins["greenPin"],self.gpioPins["bluePin"]],GPIO.OUT)
			self.RED = GPIO.PWM(int(self.gpioPins["redPin"]), 1000)
			self.GREEN = GPIO.PWM(int(self.gpioPins["greenPin"]), 1000)
			self.BLUE = GPIO.PWM(int(self.gpioPins["bluePin"]), 1000)

			self.RED.start(0)
			self.GREEN.start(0)
			self.BLUE.start(0)

	def stop(self):
		if self.showLED:
			self.RED.stop()
			self.GREEN.stop()
			self.BLUE.stop()
			GPIO.cleanup()
