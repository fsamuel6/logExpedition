# logExpedition #

## About Project ##

This python scripts logs the network connection of an Android phone. It has been tested on Google Pixel 5a and the instructions are written for this phone. The instruction might differ from android to android.

## SetUp Phone ##

1. Clone github repo
2. Connect the Samsung phone to the computer through USB/USB-c
3. On the phone:
   1. Swipe down on the top of the phone, click on "USB charging) and choose "Transferring files" option
   2. Go to Settings > Developer options > Enable "USB debugging" (or search for developer options).
      1. If you can not go to developer options: Go to Settings > About phone > Press "Build number" 5 times. Now developer options will be activated and you can do the previous task.
   3. (Only on Samsung) Dial *#8080# and choose an alternative that contains "DM" and "ADB"
4. On German SIM:
   1. Activate Roaming
   2. To allow GPS tracking: Go to Google maps, try navigating to anyplace and choose starting point as "Your location" and allow Google maps to use your location.
5. If you want to check the connection, run the command "adb devices" on your PC

## Running the script ##

Run main.py from terminal with the command "python3 main.py" or run it from an editor while leaving the USB plugged in.

The results will be saved in a folder called phoneLog in the same directory as the script. The result will be saved as .csv files, one for every time the script is executed.

## Contact Information ##
For questions, please contact fsamuel6@volvocars.com or bohman@volvocars.com
