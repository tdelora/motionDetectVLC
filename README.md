# motionDetectVLC
Python script for Raspberry Pi which detects motion and plays videos when triggered.  The script reads a yaml file for mandatory and optional parameters (See config.yml), plays an optional startup video then waits for motion and no-motion events to play specified videos. Optionally the script plays "bored" videos at a specified interval. In all cases, once a video is started it will be played to completion, subsequent events of any type will not interrupt a video in progress.

Mandatory yaml Parameters:
- starting-video (string): Video to be played when script starts.
- motion-videos (list): Videos to play when motion is detected. The list will be run in order returning to the first video when the list is exhausted.

Optional yaml Parameters:
- no-motion-video (string): Videos to play when no motion is detected.
- bored-time (int): Time in seconds between bored timer events.
- bored-videos (list): Videos to play when the bored timer fires. The list will be run in order returning to the first video when the list is exhausted.
- motion-sensor-pin (int): The GPIO pin to be read for motion events. If motion-sensor-pin is not specified the script reads from pin 12.
- vlc-fullscreen (boolean): Specifies if VLC should be run in full-screen mode. If vlc-fullscreen is not specified the script defaults to false.
- os-environment (dictionary): OS environment variables to be set as the script starts.

Hardware utilized
- iRasptek Starter Kit for Raspberry Pi 5 RAM 8GB - 64GB Edition of OS-Bookworm Pre-Loaded (Amazon)
- Link: https://a.co/d/0X1S8th
- HiLetgo 3pcs HC-SR501 PIR Infrared Sensor Human Body Infrared Motion Module for Arduino Raspberry Pi (Amazon)
- Link: https://a.co/d/7auf7Qe
- SIM&NAT 8inch / 20cm Wire Ribbon Cables kit for Arduino Raspberry Pi 2/3
- Link: https://a.co/d/fxIIGYs

Other Notes:
- Originally written as part of a Halloween jumpscare gag, it has been cleaned up for genetic use.
- starting-video and no-motion-video can be used to place the screen in an acceptable state when no video is playing. 
- Initial development was on a Raspberry Pi 3b however the device struggled with some videos, including seg faults. Problems ended with the new Raspberry Pi 5.
- VLC on Raspberry Pi works best with codec H264 videos. Codec ProRes videos do cause issues, especially in fullscreen mode.
