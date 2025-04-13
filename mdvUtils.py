#!/usr/bin/env python
import string


# Function findKey looks for a key/value pair in a data string

def findKey(data,key):
	if key in data.keys():
		# print(len(data[key]))
		# print(data[key])
		return data[key]
	else:
		# print(f"Key {key} not found")
		return None


"""
Function dictionaryUpdate iterates through an destination dictionary for like keys present in
an update dictionary calling a validation fuction before adding. If either updateDict or updateDict
args are not dictonaries or updateDict is type None (indicating there are no updates to do) argument
destDict is returned unchanged.
"""

def dictionaryUpdate(updateDict,destDict,addUnknown,validateFunc):
	returnValue = True
	tmpDict = destDict

	if type(destDict) is dict:
		updateType = type(updateDict)
		if updateType is dict:
			for key, value in updateDict.items():
				if key in destDict or addUnknown:
					# Key exists or we should add an unknown key
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
						print(f"mdvUtils.dictionaryUpdate: Adding/pdating {key} without validating")
						tmpDict[key] = value
						returnValue = False
		elif updateType is not type(None):
			# An updateType of none means there is nothing to do, any other type that is not dict or none is incorrect.
			print(f"mdvUtils.dictionaryUpdate: item received to read for updates is " + str(updateType) + " not a dictionary")
			returnValue = False
	else:
		print(f"mdvUtils.dictionaryUpdate: item received as destination is not a dictionary")
		returnValue = False

	return returnValue, tmpDict


"""
Function validateGPIOPin verifies argument pinNum is an int and in the proper range (2-27) for
Raspberry Pi GPIO pins.
"""

def validateGPIOPin(pinSpec,pinNum):
	returnValue = False
	if pinNum != None:
		if type(pinNum) is int:
			if pinNum >= 2 and pinNum <= 27:
				# A valid Raspberry Pi GPIO pin
				returnValue = True
			else:
				print(f"mdvUtils.validateGPIOPin: {pinSpec} specified as {pinNum} is out of range (2 to 27)")
		else:
			print(f"mdvUtils.validateGPIOPin: GPIO pin specification {pinSpec} is not an int")

	return returnValue


"""
Function validateHexColor verifies argument hexString is in the proper hex triplet starting with a
hashtag. Examples: #00FF00, #F9D00FF, #301934
"""

def validateHexColor(mode,hexString):
	returnValue = False
	if type(hexString) is str and len(hexString) == 7:
		if hexString[0:1] == "#":
			returnValue = all(c in string.hexdigits for c in hexString[1:])

	if returnValue == False:
		print(f"mdvUtils.validateHexColor: {hexString} for specification '{mode}' is an invalid color hex string")

	return returnValue


"""
Function colorHexTo8bit takes a hex triplet string and converts it to its equal 8 bit specifications.
Example: #301934 -> R: 48 G: 25 B: 52
"""

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
