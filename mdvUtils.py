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

def dictionaryUpdate(updateDict,destDict,validateFunc):
	returnValue = True
	tmpDict = destDict

	if type(destDict) is dict:
		updateType = type(updateDict)
		if updateType is dict:
			for key in tmpDict.keys():
				value = findKey(updateDict,key)
				if value != None:
					if validateFunc != None:
						# Check each potential change, if any come back false change returnValue to False
						# Doing it this way reveals all issues in the dictionary
						validateReturnValue = validateFunc(key,value)
						if validateReturnValue:
							# All good for this one
							tmpDict[key] = value
						else:
							# We encountered an issue
							returnValue = False
					else:
						print(f"mdvUtils.dictionaryUpdate: Updating {key} without validating")
						tmpDict[key] = value
						returnValue = False
		elif updateType is not type(None):
			print(f"mdvUtils.dictionaryUpdate: item received to read for updates is " + str(updateType) + " not a dictionary")
			returnValue = False
	else:
		print(f"mdvUtils.dictionaryUpdate: item received as destination is not a dictionary")
		returnValue = False

	return returnValue, tmpDict


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


def validateHexColor(mode,hexString):
	returnValue = False
	if type(hexString) is str and len(hexString) == 7:
		if hexString[0:1] == "#":
			returnValue = all(c in string.hexdigits for c in hexString[1:])

	if returnValue == False:
		print(f"mdvUtils.validateHexColor: {hexString} for specification '{mode}' is an invalid color hex string")

	return returnValue


def colorHexTo8bit(hexString):
	redVal = 0
	greenVal = 0
	blueVal = 0

	if validateHexColor("mdvUtils.colorHexTo8bit",hexString):
		redVal = int(hexString[1:3],16)
		greenVal = int(hexString[3:5],16)
		blueVal = int(hexString[5:],16)
		# print(f"colorHexTo8bit: {hexString}: r:{redVal} g:{greenVal} b:{blueVal}")

	return redVal, greenVal, blueVal
