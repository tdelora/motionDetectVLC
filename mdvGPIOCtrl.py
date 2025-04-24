"""
This Raspberry Pi code was developed with assistence from newbiely.com
newbiely.com Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-led-rgb

Thank you newbiely.com
"""

from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import mdvUtils
import time

"""
Class gpioCtrlClass is a GPIO pin controller class.
"""

class gpioCtrlClass:

	# GPIO layout 
	gpioPins = {'redPin':13,'greenPin':6,'bluePin':18,'buttonPin':16,'motionPin':12}

	# Motion detection variables
	pirSensor = None

	# LED Ops variables
	showLED = True
	ledStatusColors = {'start':"#FF0000",'bored':"#0000FF",'no_motion':"#ff8000",'motion':"#301934",'waiting':"#00FF00"}

	# Button Ops variables
	buttonOps = True
	buttonCallable = None
	buttonPressTime = 0

	# Misc variables
	addUnknown = False

	# Function __init__ is the initializer for this class.

	def __init__(self):
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


	# Function buttonEvent is the callback for both button press and release events.
	# In release events the function will calculate the duration of the button press
	# and pass it along to self.buttonCallable, where the user can act on the event. 

	def buttonEvent(self,channel):

		if GPIO.input(self.gpioPins["buttonPin"]):
			# The button has been pressed, mark the time.
			self.buttonPressTime = time.time()
		else:
			# The button has been released
			buttonReleaseTime = time.time()
			elapsed_time = buttonReleaseTime - self.buttonPressTime

			# By this time self.buttonCallable should have been verified to be a callable.
			# However lets check because I am paranoid...
			if callable(self.buttonCallable):
				self.buttonCallable(elapsed_time)
			else:
				print("mdvGPIOCtrl.buttonEDvent: self.buttonCallable is uncalable type " + type(self.buttonCallable))


	# Function configure receives dictionary gpioConfig and updates class gpioCtrlClass dictionaries
	# gpioPins and ledStatusColors as needed.
	# Note: mdvUtils.mdvUtils.dictionaryUpdate() optionally can add new values to a receive destionation
	# dictionary, this function is not taking advantage of that. Yet.

	def configure(self,gpioConfig):
		returnValue = True

		if type(gpioConfig) is dict:

			# Check for new showLED state
			tmpBool = mdvUtils.findKey(gpioConfig,"led-status")
			if type(tmpBool) is bool:
				self.showLED = tmpBool
			elif tmpBool != None:
				print(f"mdvLED.configure: Value received for led-status is a " + type(tmpBool) + "not a boolean")
				returnValue = False

			# Check for new buttonOps state
			tmpBool = mdvUtils.findKey(gpioConfig,"button-ops")
			if type(tmpBool) is bool:
				self.buttonOps = tmpBool
			elif tmpBool != None:
				print(f"mdvLED.configure: Value received for button-ops is a " + type(tmpBool) + "not a boolean")
				returnValue = False

			# Check if the dictionaries should add unknown key/value pairs.
			tmpBool = mdvUtils.findKey(gpioConfig,"add-unknown-pairs")
			if type(tmpBool) is bool:
				self.addUnknown = tmpBool
			elif tmpBool != None:
				print(f"mdvLED.configure: Value received for add-unknown-pairs is a " + type(tmpBool) + "not a boolean")
				returnValue = False

			# Check each dictionary seperately so all issues will be displayed at once vs one at a time
			pinReturnValue, self.gpioPins = mdvUtils.dictionaryUpdate(mdvUtils.findKey(gpioConfig,"gpioPins"),self.gpioPins,self.addUnknown,mdvUtils.validateGPIOPin)
			modeReturnValue, self.ledStatusColors = mdvUtils.dictionaryUpdate(mdvUtils.findKey(gpioConfig,"ledStatusColors"),self.ledStatusColors,self.addUnknown,mdvUtils.validateHexColor)
			if pinReturnValue != True or modeReturnValue != True:
				# One of the dictionaries had an issue
				returnValue = False
		elif gpioConfig != None:
			print(f"mdvLED.configure: Received config info is not a dictionary")
			returnValue = False

		# print(f"gpioPins: {self.gpioPins}")
		# print (f"ledStatusColors: {self.ledStatusColors}")
		# print(f"pinReturnValue: {pinReturnValue}")
		# print(f"modeReturnValue: {modeReturnValue}")
		# print(f"returnValue: {returnValue}")

		return returnValue


	# Function start sets up the GPIO configuration specified in dictionary gpioPins, calls start if bool showLED is set to true
	# and sets up for button operations if buttonOps is True and userButtonCallable is a callable.

	def start(self,motionCallable,noMotionCallable,userButtonCallable):
		returnValue = True

		# Verify the callables
		if callable(motionCallable) != True:
			print(f"gpioCtrlClass.start: Received motionCallable is uncallable type " + type(userButtonCallable))
			returnValue = False

		if callable(noMotionCallable) != True:
			print(f"gpioCtrlClass.start: Received noMotionCallable is uncallable type " + type(userButtonCallable))
			returnValue = False

		if callable(userButtonCallable) != True:
			print(f"gpioCtrlClass.start: Received userButtonCallable is uncallable type " + type(userButtonCallable))
			returnValue = False

		# If returnValue is True then we are good to start
		if returnValue:
			self.pirSensor = MotionSensor(self.gpioPins["motionPin"])
			self.pirSensor.when_motion = motionCallable
			self.pirSensor.when_no_motion = noMotionCallable

			if self.showLED:
				GPIO.setup([self.gpioPins["redPin"], self.gpioPins["greenPin"],self.gpioPins["bluePin"]],GPIO.OUT)
				self.RED = GPIO.PWM(int(self.gpioPins["redPin"]), 1000)
				self.GREEN = GPIO.PWM(int(self.gpioPins["greenPin"]), 1000)
				self.BLUE = GPIO.PWM(int(self.gpioPins["bluePin"]), 1000)

				self.RED.start(0)
				self.GREEN.start(0)
				self.BLUE.start(0)

			if self.buttonOps:
				if userButtonCallable != None:
					# The user has passed us somthing usable
					if callable(userButtonCallable):
						# ... and it is a function. Set buttonCallable to point to userButtonCallable
						# and set up for button ops.
						self.buttonCallable = userButtonCallable
						GPIO.setup(self.gpioPins["buttonPin"], GPIO.IN)
						GPIO.add_event_detect(self.gpioPins["buttonPin"],GPIO.BOTH,callback=self.buttonEvent)
					else:
						print(f"gpioCtrlClass.start: userButtonCallable is uncallable type " + type(userButtonCallable) + ", button ops disabled.")

			# Finally set the LED color to the start color
			self.setColor(self.ledStatusColors['start'])

		return returnValue

	# Function stop calls stop for the specified GPIO.PWM pins  if bool showLED is set to true.

	def stop(self):
		if self.showLED:
			self.RED.stop()
			self.GREEN.stop()
			self.BLUE.stop()

		GPIO.cleanup()
