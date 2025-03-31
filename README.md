# motionDetectVLC
Python script for Raspberry Pi which detects motion and plays videos when triggered.





Hardware utilized
- iRasptek Starter Kit for Raspberry Pi 5 RAM 8GB - 64GB Edition of OS-Bookworm Pre-Loaded (Amazon)
- Link: https://a.co/d/0X1S8th
- HiLetgo 3pcs HC-SR501 PIR Infrared Sensor Human Body Infrared Motion Module for Arduino Raspberry Pi
- Link: https://a.co/d/7auf7Qe

Other Notes:
- Initial development was on a Raspberry Pi 3b however the device struggled with some videos, including seg faults. Problems ended with the new Raspberry Pi 5.
- VLC had issues running codec ProRes videos fullscreen, the same videos ran fine when VLC was not in fullscreen. This issue did not occur with codec H264 videos.
