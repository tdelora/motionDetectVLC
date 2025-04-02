#!/usr/bin/env python

from gpiozero import MotionSensor
import os
from pathlib import Path
from signal import pause
import sys
import threading
import time
import vlc
import yaml

#OS environment setup
osEnvironment = ""

# Initial VLC setup: Create VLC instance and player
vlcInstance = vlc.Instance()
vlcPlayer = vlcInstance.media_player_new()

# Other VLC related variables
vlcFullscreen = False

# Motion sensor setup
motionSensorPin = 12
triggers = 0

# Video to play when the program starts
startingVideo = ""

# Variables and lists for videos used when motion is detected.
currentMotionVideo = 0
# Video list for motion detected events
motionVideoList = ""

# Video for no motion events (if required)
noMotionVideo = ""

# The boredTimer is triggered every <timeUntilBored> seconds and runs the specified video.
#   - Set timeUntilBored to 0 (zero) to deactivate this capability.
#   - Note that fuction playVideo will not play a video if another is already playing. 
boredTimer = threading.Timer(1,None)
timeUntilBored = 180
currentBoredVideo = 0
boredVideoList = ""

try:

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


	#
	# Function loadVerifyConfig reads the configuration yaml
	#  - Verifies the specified file exists before reading it
	#  - Sets specified variable values
	#  - Verifies any videos listed can be found
	#  - Will return False if certain videos are not specified.
	#

	def loadVerifyConfig(configFile):
		global osEnvironment
		global startingVideo
		global motionVideoList
		global noMotionVideo
		global timeUntilBored
		global boredVideoList
		global vlcFullscreen
		global motionSensorPin
		returnValue = True

		fileCheck = Path(configFile)
		if fileCheck.exists():
			with open(configFile,"r") as file:
				data = yaml.safe_load(file)

			# Verify user provided configuration

			# Verify startingVideo (Manditory)
			startingVideo = findKey(data,"starting-video")
			fileCheck = Path(startingVideo)
			if fileCheck.exists() == False:
				print(f"Starting video {startingVideo} does not exist")
				returnValue = False

			# Verify motionVideoList (Manditory)
			motionVideoList = findKey(data,"motion-videos")
			if type(motionVideoList) is list:
				currentFile = 0
				while currentFile < len(motionVideoList):
					# print(motionVideoList[currentFile])
					fileCheck = Path(motionVideoList[currentFile])
					if fileCheck.exists() == False:
						removedFile = motionVideoList.pop(currentFile)
						print(f"Motion video {removedFile} does not exist - removed from list")
						currentFile -= 1
					currentFile += 1
				if len(motionVideoList) == 0:
					# Nothing survived the pruning...
					print("Motion video list is empty - aborting")
					returnValue = False
			else:
				print(f"motion-videos specified in {configFile} is not a list")
				returnValue = False

			# Verify noMotionVideo (Optional)
			noMotionVideo = findKey(data,"no-motion-video")
			if noMotionVideo != None:
				fileCheck = Path(noMotionVideo)
				if fileCheck.exists() == False:
					# Bad but surivable...
					print(f"No motion video {noMotionVideo} does not exist - functionality disabled")
					noMotionVideo = ""

			# Verify boredVideoList (Optional)
			boredVideoList = findKey(data,"bored-videos")
			if boredVideoList != None:
				if type(boredVideoList) is list:
					currentFile = 0
					while currentFile < len(boredVideoList):
						# print(boredVideoList[currentFile])
						fileCheck = Path(boredVideoList[currentFile])
						if fileCheck.exists() == False:
							removedFile = boredVideoList.pop(currentFile)
							print(f"Bored video {removedFile} does not exist - removed from list")
							currentFile -= 1
						currentFile += 1
					if len(boredVideoList) == 0:
						# Nothing survived the pruning however this is survivable. But no bored videos will run.
						timeUntilBored = 0
						print("Bored video list is empty - bored timer disabled")
				else:
					print(f"bored-videos specified in {configFile} is not a list")
					returnValue = False

			# The bored timer has a default of 180 seconds, check if an updated value has been provided.
			tempTime = findKey(data,"bored-time")
			if tempTime != None:
				if type(tempTime) is int:
					timeUntilBored = tempTime
				else:
					print(f"bored-time specified in {configFile} is not an int")
					returnValue = False

			# vlcFullscreen has a default value of True, check if an updated value has been provided.
			vlcFullscreenTmp = findKey(data,"vlc-fullscreen")
			if type(vlcFullscreenTmp) is bool:
				vlcFullscreen = vlcFullscreenTmp
			else:
				print(f"vlc-fullscreen specified in {configFile} is not a bool")

			# Set motionSensorPin (Optional, Defaulted to pin 12)
			motionSensorPinTmp = findKey(data,"motion-sensor-pin")
			if motionSensorPinTmp != None:
				if type(motionSensorPinTmp) is int:
					if motionSensorPinTmp >= 2 and motionSensorPinTmp <= 27:
						# A valid Raspberry Pi GPIO pin
						motionSensorPin = motionSensorPinTmp
					else:
						print(f"motion-sensor-pin specified as {motionSensorPinTmp} in {configFile} is out of range (2 to 27)")
						returnValue = False
				else:
					print(f"motion-sensor-pin specified in {configFile} is not an int")
					returnValue = False

			# Load optional environment settings. This will be checked/used in main()
			osEnvironment = findKey(data,"os-environment")
		else:
			print(f"{configFile} does not exist")
			returnValue = False

		return returnValue


	#
	# Function playVideo checks for the existence of a file videoFile, plays it if it exists
	#   - Checks for videoFile, plays it if it exists
	#   - Waits 3 seconds as the video starts
	#   - Waits for the video to complete
	#   - Logs an error if videoFile does not exist.
	#

	def playVideo(videoFile):
		videoCheck = Path(videoFile)
		returnValue = True

		if videoCheck.exists():
			if vlcPlayer.is_playing() != True:
				print(f"Playing {videoFile}")
				media = vlcInstance.media_new_path(videoFile)
				vlcPlayer.set_media(media)
				vlcPlayer.play()
				time.sleep(3)
				while vlcPlayer.is_playing():
					time.sleep(1)
			else:
				print()
				print("A video is currently playing")
		else:
			print
			print(f"Cannot find file {videoFile}")
			print
			returnValue = False
		return returnValue


	#
	# Function motionDetected is called when motion is detected.
	#   - Updates the trigger count and notifies the user
	#   - Passes the current video to funtion playVideo
	#   - Updates the current video and resets the count if we are at the end of the list
	#   - Waits for the video to complete
	#   - Restarts the bored timer
	#

	def motionDetected():
		global triggers
		global currentMotionVideo
		global motionVideoList

		triggers = triggers + 1
		print()
		print(f"Motion {triggers} detected...")

		playVideo(motionVideoList[currentMotionVideo])

		currentMotionVideo += 1
		if currentMotionVideo == len(motionVideoList):
			currentMotionVideo = 0
		print("Motion detected complete")


	#
	# Function noMotionDetected is called when no motion is detected.
	#   - Notifies the user
	#

	def noMotionDetected():
		print()
		print("No motion...")
		if noMotionVideo != None and len(noMotionVideo):
			playVideo(noMotionVideo)
		print("No motion detected complete")


	#
	# Function setBoredTimer sets the bored time so a video will run every <timeUntilBored> seconds.
	#   - If timeUntilBored is zero the timer will not be set.
	#

	def setBoredTimer():
		global boredTimer

		# If timeUntilBored is zero do not run timer.
		if timeUntilBored != 0:
			print(f"Setting bored timer for {timeUntilBored} seconds")
			boredTimer = threading.Timer(timeUntilBored,imBored).start()
		else:
			print("Not setting bored timer")


	#
	# Function imBored is executed when the bored timer fires.
	#   - Video <boredVideo> will be passed to function playVideo.
	#   - Function setBoredTimer is called to restart the bored timer.
	#

	def imBored():
		global boredVideoList
		global currentBoredVideo

		print()
		print("I'm bored...")
		playVideo(boredVideoList[currentBoredVideo])
		currentBoredVideo += 1
		if currentBoredVideo == len(boredVideoList):
			currentBoredVideo = 0
		setBoredTimer()
		print("No longer bored...")


	#
	# Function main is the program entry point
	#   - Triggers the config yaml to be read
	#   - Sets any specified global variables
	#   - Sets the VLC full screen setting.
	#   - Sets the PIR when_motion and when_no_motion functions
	#   - Notifies the user PIR motion sensor detection is starting
	#   - Starts the bored timer
	#   - Triggers the starting video 
	#   - Calls pause to sleep the process.
	#

	def main():
		if len(sys.argv) > 1:
			configFile = sys.argv[1]
			# print(configFile)

			if loadVerifyConfig(configFile):
				# print(f"startingVideo: {startingVideo}")
				# print(f"motionVideoList: {motionVideoList}")
				# print(f"timeUntilBored: {timeUntilBored}")
				# print(f"boredVideoList: {boredVideoList}")

				if len(osEnvironment) != 0 and type(osEnvironment) is dict:
					# Environment variables have been provided as a dictionary
					for key,value in osEnvironment.items():
						os.environ[key] = value

				vlcPlayer.set_fullscreen(vlcFullscreen)

				pir = MotionSensor(motionSensorPin)
				pir.when_motion = motionDetected
				pir.when_no_motion = noMotionDetected
				print("Detection started")
				print()

				setBoredTimer()
				playVideo(startingVideo)

				pause()
		else:
			print()
			print("Please provide a config yaml file")
			print()

	if __name__ == "__main__":
		main()

finally:
	# Future features
	print()
	print("Closing down")
