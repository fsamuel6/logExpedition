# This is a Python script for logging the connection status of a Samsung phone

import subprocess
from datetime import datetime
import time

while True:
    connection_status = subprocess.check_output(["adb", "shell", "dumpsys", "telephony.registry"]).decode("utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "nrState=CONNECTED" in connection_status:
        print(f"{timestamp}: Phone connected to 5G")
        with open("connection_log.txt", "a") as log_file:
            log_file.write(f"{timestamp}: Phone connected to 5G\n")
    elif "mDataConnectionState=2" in connection_status:
        print(f"{timestamp}: Phone connected to 4G")
        with open("connection_log.txt", "a") as log_file:
            log_file.write(f"{timestamp}: Phone connected to 4G\n")
    elif "mDataConnectionState=0" in connection_status:
        print(f"{timestamp}: Phone disconnected from 4G or 5G")
        with open("connection_log.txt", "a") as log_file:
            log_file.write(f"{timestamp}: Phone disconnected from 4G or 5G\n")

    time.sleep(1)
