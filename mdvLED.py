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

"""
Class ledStatusClass is a GPIO LED pin controller class.
"""

class ledStatusClass:

	gpioPins = {'redPin':13,'greenPin':6,'bluePin':18}
	statusModes = {'start':"#FF0000",'bored':"#0000FF",'no_motion':"#ff8000",'motion':"#301934",'waiting':"#00FF00"}
	
	# Function __init__ is the initializer for this class.

	def __init__(self):
		self.showLED = False
		GPIO.setmode(GPIO.BCM)


	# Function _duty sets the RGB values for the LED. This code came from newbiely.com. Again, thank you.

	def _duty(self,x, in_min, in_max, out_min, out_max):
    		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


	# Function setColor receives a hex color string, has it converted to 8-bit color specification
	# and calls _duty() to set the LED color.

	def setColor(self,hexString):
		if self.showLED:
			redVal, greenVal, blueVal = mdvUtils.colorHexTo8bit(hexString)
			# print(f"mdvLED.setColor: r:{redVal} g:{greenVal} b:{blueVal}")
			self.RED.ChangeDutyCycle(self._duty(redVal, 0, 255, 0, 100))
			self.GREEN.ChangeDutyCycle(self._duty(greenVal, 0, 255, 0, 100))
			self.BLUE.ChangeDutyCycle(self._duty(blueVal, 0, 255, 0, 100))


	# Function configure receives dictionary ledConfig and updates class ledStatusClass dictionaries
	# gpioPins and statusModes as needed.
	# Note: mdvUtils.mdvUtils.dictionaryUpdate() optionally can add new values to a receive destionation
	# dictionary, this function is not taking advantage of that. Yet.

	def configure(self,ledConfig):
		returnValue = True
		addUnknown = False

		if type(ledConfig) is dict:
			# Check each dictionary seperately so all issues will be displayed at once vs one at a time
			pinReturnValue, self.gpioPins = mdvUtils.dictionaryUpdate(mdvUtils.findKey(ledConfig,"gpioPins"),self.gpioPins,addUnknown,mdvUtils.validateGPIOPin)
			modeReturnValue, self.statusModes = mdvUtils.dictionaryUpdate(mdvUtils.findKey(ledConfig,"statusModes"),self.statusModes,addUnknown,mdvUtils.validateHexColor)
			if pinReturnValue != True or modeReturnValue != True:
				# One of the dictionaries had an issue
				returnValue = False
		elif ledConfig != None:
			print(f"mdvLED.configure: Received config info is not a dictionary")
			returnValue = False

		# print(f"gpioPins: {self.gpioPins}")
		# print (f"statusModes: {self.statusModes}")
		# print(f"pinReturnValue: {pinReturnValue}")
		# print(f"modeReturnValue: {modeReturnValue}")
		# print(f"returnValue: {returnValue}")

		return returnValue


	# Function start sets up the GPIO configuration specified in dictionary gpioPins and calls start if bool showLED is set to true.

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


	# Function stop calls stop for the specified GPIO.PWM pins  if bool showLED is set to true.

	def stop(self):
		if self.showLED:
			self.RED.stop()
			self.GREEN.stop()
			self.BLUE.stop()
			GPIO.cleanup()
