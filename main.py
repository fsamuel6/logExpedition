# This is a Python script for logging the connection status of a Samsung phone

import subprocess
from datetime import datetime
import time
import os
import csv

## Set up a folder and a new log file for each run
def setUp():
    # Some information for the file
    time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    column_heads = ["timestamp", "apn1", "apn2", "connection_state", "technology", "raw_rssi", "rssi", "ber", "rscp",
                    "rsrp", "rsrq", "mcc", "mnc", "network_provider", "operator", ]

    # make folder if not exists
    current_working_directory = os.getcwd() + "/phone_log"
    if not os.path.exists(current_working_directory):
        os.makedirs(current_working_directory)

    # make new file
    file_path = current_working_directory + "/connection_log_" + time + ".csv"
    open(file_path, "x")  # Creates file
    file = open(file_path, "a")

    # Add column heads to file
    csv.writer(file).writerow(column_heads)
    file.close()

    return file_path

## Main method ##
def main():
    # Open file we created in write mode
    f = open(setUp(), "a");
    writer = csv.writer(f)

    while True:
        connection_status = subprocess.check_output(["adb", "shell", "dumpsys", "telephony.registry"]).decode("utf-8")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        apn1 = "null"
        apn2 = "null"
        connection_state = "null"
        technology = "null"
        raw_rssi = "null"
        rssi = "null"
        ber = "null"
        rscp = "null"
        rsrp = "null"
        rsrq = "null"
        mcc = "null"
        mnc = "null"
        network_provider = "null"
        operator = "null"

        if "nrState=CONNECTED" in connection_status:
            # print(f"{timestamp}: Phone connected to 5G")
            connection_state = "connectedRoaming"
            technology = "nr"

        elif "mDataConnectionState=2" in connection_status:
            # print(f"{timestamp}: Phone connected to 4G")
            connection_state = "connectedRoaming"
            technology = "lte"

        elif "mDataConnectionState=0" in connection_status:
            # print(f"{timestamp}: Phone disconnected from 4G or 5G")
            connection_state = "Not Connected"
            technology = "none"

        # write data to file
        row = [timestamp, apn1, apn2, connection_state, technology, raw_rssi, rssi, ber, rscp, rsrp, rsrq, mcc, mnc,
               network_provider, operator]

        print(row)
        writer.writerow(row)

        # Vi kan behöva räkna bort hur lång tid scriptet tar att köra, annars kommer tiderna förskjutas. Men
        # det gör det i Serdars script också.
        time.sleep(3)  # for testing
        # time.sleep(10) # Ska logga var 10e sekund

    # Addera så scriptet inte slutar på error
    # filen ska stängas
    # f.close()


## Run script ##
if __name__ == "__main__":
    main()
