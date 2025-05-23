# motionDetectVLC
Python script for Raspberry Pi which detects motion and plays videos when triggered.  The script reads a yaml file for mandatory and optional parameters (See config.yml), plays an optional startup video, and then waits for motion and no-motion events to play specified videos. Optionally the script plays "bored" videos at a specified interval. In all cases, once a video is started it will be played to completion, subsequent events of any type will not interrupt a video in progress.

Optional Functionality:
- The current script status can be displayed on an attached LED, there are default GPIO pin and status color settings, which can be changed in the yaml file to the user-desired specifications.
- A button can be utilized to control some operations:
  - A press of less than 5 seconds will toggle the VLC player in and out of full screen mode.
  - A press of more than 5 seconds will trigger the script to exit.

Mandatory yaml Parameters:
- starting-video (string): Video to be played when script starts.
- motion-videos (list): Videos to play when motion is detected. The list will be run in order returning to the first video when the list is exhausted.

Optional yaml Parameters:
- no-motion-video (string): Videos to play when no motion is detected.
- bored-time (int): Time in seconds between bored timer events.
- bored-videos (list): Videos to play when the bored timer fires. The list will be run in order returning to the first video when the list is exhausted.
- vlc-fullscreen (boolean): Specifies if VLC should be run in full-screen mode. If vlc-fullscreen is not specified the script defaults to false.
- os-environment (dictionary): OS environment variables to be set as the script starts.

Optional GPIO Parameters:
- gpio-config (dictionary): Dictionary for GPIO pins, LED status color and other related settings. Not all dictionaries or dictionary entries are needed, if a setting is not specified the default values are utilized. Member key/value pairs:
    - led-status (boolean): Enable the LED status operations. Default: True
    - button-ops (boolean): Enable the button operations. Default: True
    - add-unknown-pairs (boolean): Allow the yaml configuration file to add entries to the dictionaries. Default: False
    - gpioPins (dictionary): GPIO pins to be used for LED and button operations.
      - redPin (int): Pin for red. Default: 13
      - greenPin (int): Pin for green. Default: 6
      - bluePin (int): Pin for blue. Default: 18
      - buttonPin (int): Pin for the button signal. Default: 16
      - motionPin (int): Pin for the PIR motion detection. Default: 12
    - ledStatusColors (dictionary): LED colors for the various script status modes. Modes are:
      - start (string): Color displayed in the startup phase. Default: #FF0000 (red)
      - bored (string): Color displayed when bored videos are playing. Default: #0000FF (blue)
      - no_motion (string): Color displayed when a no-motion event occurs. Default: #ff8000 (orange)
      - motion (string): Color displayed when a motion event occurs. Default: #301934 (dark purple)
      - waiting (string): Color displayed between events or timer firings. Default: #00FF00 (green)

Hardware utilized (Ordered from Amazon):
- iRasptek Starter Kit for Raspberry Pi 5 RAM 8GB - 64GB Edition of OS-Bookworm Pre-Loaded
  - Link: https://a.co/d/0X1S8th
- HiLetgo 3pcs HC-SR501 PIR Infrared Sensor Human Body Infrared Motion Module for Arduino Raspberry Pi
  - Link: https://a.co/d/7auf7Qe
- RGB LED Module for Arduino, ESP32, ESP8266, Raspberry Pi, 10 Pieces
  - Link: https://a.co/d/4fR2OXq
- WWZMDiB 6Pcs TTP223B Digital Capacitive Touch Sensor Switch
  - https://a.co/d/4RpuDDr
- SIM&NAT 8inch / 20cm Wire Ribbon Cables kit for Arduino Raspberry Pi 2/3
  - Link: https://a.co/d/fxIIGYs

Other Notes:
- Originally written as part of a Halloween jumpscare gag, it has been cleaned up for genetic use.
- starting-video and no-motion-video can be used to place the screen in an acceptable state when no video is playing. 
- Boolean add-unknown-pairs in the gpio-config allows new key/value pairs to be added to the dictionary making the the dictionaries and class to be extensable without code changes.
- Initial development was on a Raspberry Pi 3b however the device struggled with some videos, including seg faults. Problems ended with the new Raspberry Pi 5.
- VLC on Raspberry Pi works best with codec H264 videos. Codec ProRes videos do cause issues, especially in fullscreen mode.
