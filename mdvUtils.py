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
