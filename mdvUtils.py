#!/usr/bin/env python

def validateGPIOPin(pinSpec,pinNum):
	returnValue = False
	if pinNum != None:
		if type(pinNum) is int:
			if pinNum >= 2 and pinNum <= 27:
				# A valid Raspberry Pi GPIO pin
				returnValue = True
			else:
				print(f"{pinSpec} specified as {pinNum} is out of range (2 to 27)")
		else:
			print(f"GPIO pis specification {pinSpec} is not an int")

	return returnValue


def validateHexColor(hexColor):
	returnValue = False
	if hexColor != None:
		if len(hexColor) == 7 and type(hexColor) is str:
			print("good")

	return returnValue


def colorHexTo8bit(hexString):
	redVal = 0
	greenVal = 0
	blueVal = 0

	if type(hexString) is str and len(hexString) == 7:
		redVal = int(hexString[1:3],16)
		greenVal = int(hexString[3:5],16)
		blueVal = int(hexString[5:],16)
		# print(f"colorHexTo8bit: {hexString}: r:{redVal} g:{greenVal} b:{blueVal}")
	else:
		print(f"colorHexTo8bit: Not a string or not a valid hex color string length: {hexString}")

	return redVal, greenVal, blueVal
