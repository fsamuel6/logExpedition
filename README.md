# logExpedition #

## About Project ##

This python scripts logs the network connection of an Android phone. It has been tested on Google Pixel 5a and the instructions are written for this phone. The instruction might differ from android to android.

## First Setup of Phone ##

1. Clone github repo
2. On German SIM:
   1. Settings -> Connections -> Mobile networks -> Turn on Data Roaming
3. On the phone:
   1. Call *#0808# -> DM and ADB 
   2. Go to Settings -> About phone -> Software information -> Build number and press 5 times 
   3. Go to Settings -> System -> Developer options -> USB debugging (on)
   4. Connect phone to usb cable and “Allow USB debugging” 
   5. Swipe down, press “USB charging” -> choose “File transfer” 
   6. To allow GPS tracking: Go to Google maps, try navigating to any place and choose starting point as "Your location" and allow Google maps to use your location.
4. If you want to check the connection, run the command "adb devices" on your PC

## Everyday Setup ##
1. Plugin in usb
2. Swipe down, press “USB charging” -> choose “File transfer” 

## Running the script ##
Run main.py from terminal with the command "python3 main.py" or run it from an editor while leaving the USB plugged in.

The results will be saved in a folder called phoneLog in the same directory as the script. The result will be saved as .csv files, one for every time the script is executed.

## Contact Information ##
For questions, please contact fsamuel6@volvocars.com or bohman@volvocars.com
