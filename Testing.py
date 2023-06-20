# This is a Python script for logging the connection status of a Samsung phone

import subprocess
from datetime import datetime
import time
import os
import csv


def get_network_type():
    result = subprocess.run(['adb', 'shell', 'getprop', 'gsm.network.type'], capture_output=True)
    output = result.stdout.decode().strip()
    print(result)
    if 'lte' in output.lower():
        return '4G'
    elif '3g' in output.lower():
        return '3G'
    elif '2g' in output.lower():
        return '2G'
    elif 'nr' in output.lower():
        return '5G'
    else:
        return 'none'

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
    global connection_state, technology
    f = open(setUp(), "a");
    writer = csv.writer(f)

    i=0 #For testing
    #while True:
    while True:
        network_type = get_network_type()
        print("Network type: " + network_type)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tech_index = 0 # Gives index of information about 2G, 3G, 4G or 5G when parsing some input
        apn1 = "0"
        apn2 = "0"
        raw_rssi = "0"
        rssi = "0"
        ber = "0"
        rscp = "0"
        rsrp = "0"
        rsrq = "0"
        mcc = "-"
        mnc = "-"
        network_provider = "-"
        operator = "-"

        ## Connection state and technology
        connection_status = subprocess.check_output(["adb", "shell", "dumpsys", "telephony.registry"]).decode("utf-8")
        #print(connection_status)
        output = subprocess.check_output(
            ['adb', 'shell', 'dumpsys', 'telephony.registry', '|', 'grep', 'mSignalStrength']).decode().strip()

        # Connection to 4G
        if network_type == "4G": #eller: mDataConnectionType=13"
        #if "mDataConnectionType=13" in connection_status:  # eller: mDataConnectionType=13"
            connection_state = "connectedRoaming"
            technology = "lte"

            signal_strength = output.split(',')[4].split(" ")  # Splitting ouput to get valuable information
            #print(signal_strength)
            rssi = signal_strength[1].replace("rssi=", "")
            rsrp = signal_strength[2].replace("rsrp=", "")
            rsrq = signal_strength[3].replace("rsrq=", "")

        # Connection to 3G
        elif network_type == "3G":
            connection_state = "connectedRoaming"
            technology = "wcdma"
            signal_strength = output.split(',')[2].split(" ")  # Splitting ouput to get valuable information
            rsrp = signal_strength[3].replace("rsrp=", "")
            ber = signal_strength[2].replace("ber=", "")

        # Connection to 2G
        elif network_type == "2G":
            connection_state = "connectedRoaming"
            technology = "gsm"
            signal_strength = output.split(',')[1].split(" ")  # Splitting ouput to get valuable information
            rssi = signal_strength[1].replace("rssi=", "")
            ber = signal_strength[2].replace("ber=", "")
        # Connection to 5G
        elif network_type == "5G":
            connection_state = "connectedRoaming"
            technology = "nr"
            signal_strength = output.split(',')[5].split(" ")  # Splitting ouput to get valuable information

            #Nedan gissar jag att dessa finns
            rssi = signal_strength[1].replace("rssi=", "")

        # No connection
        elif network_type == "none":
            # print(f"{timestamp}: Phone disconnected from 4G or 5G")
            connection_state = "Not Connected"
            technology = "none"
            tech_index = 0

        # write data to file
        input_line = [timestamp, apn1, apn2, connection_state, technology, raw_rssi, rssi, ber, rscp, rsrp, rsrq, mcc, mnc,
               network_provider, operator]
        writer.writerow(input_line)

        # Vi kan behöva räkna bort hur lång tid scriptet tar att köra, annars kommer tiderna förskjutas. Men
        # det gör det i Serdars script också.
        time.sleep(3)  # for testing
        # time.sleep(10) # Ska logga var 10e sekund

       # i+=1 # for testing
## Run script ##
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted")
