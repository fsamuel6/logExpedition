# logExpedition

Expedition log instructions

1. Connect the Samsung phone to the computer through USB/USB-c
2. On the phone:
   a. Dial *#8080# and choose an alternative that contains "DM" and "ADB"
   b. Swipe down on the top of the phone, choose the USB settinga and choose "Transferring files" option
   c. Go to Settings > Developer options > Enable "USB debugging".
     - If you can not go to developer options: Go to Seetings > About phone > Software information > Press "Build number" 7 times. Now developer options will be activated
4. If you want to check the connection, Run the command "adb devices" on your PC
5. Run main.py from terminal with the command "python3 main.py" or run it from an editor
   - The results will be saved in a folder called phoneLog in the same directory as the script . The result will e saved as .csv files; one for every time the script is exacuted
