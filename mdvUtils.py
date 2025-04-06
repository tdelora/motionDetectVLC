#!/usr/bin/env python
import string


#
# Function findKey looks for a key/value pair in a data string
#

def findKey(data,key):
	if key in data.keys():
		# print(len(data[key]))
		# print(data[key])
		return data[key]
	else:
		# print(f"Key {key} not found")
		return None


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


def validateHexColor(hexString):
	returnValue = False
	if type(hexString) is str and len(hexString) == 7:
		if hexString[0:1] == "#":
			returnValue = all(c in string.hexdigits for c in hexString[1:])

	if returnValue == False:
		print(f"mdvUtils.validateHexColor: {hexString} is an invalid color hex string")

	return returnValue


def colorHexTo8bit(hexString):
	redVal = 0
	greenVal = 0
	blueVal = 0

	if validateHexColor(hexString):
		redVal = int(hexString[1:3],16)
		greenVal = int(hexString[3:5],16)
		blueVal = int(hexString[5:],16)
		# print(f"colorHexTo8bit: {hexString}: r:{redVal} g:{greenVal} b:{blueVal}")

	return redVal, greenVal, blueVal
