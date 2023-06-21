# This is a Python script for logging the connection status of a Samsung phone

import subprocess
from datetime import datetime
import time
import os
import csv


def get_network_type():
    result = subprocess.run(['adb', 'shell', 'getprop', 'gsm.network.type'], capture_output=True)
    output = result.stdout.decode().strip().lower()
    print("Network connection: " + output)
    if 'lte' in output:
        return '4G'
    elif "edge" in output:
        return '2G'
    elif "hspap" in output or 'umts' in output or 'wcdma' in output:
        return '3G'
    elif 'nr' in output:
        return '5G'
    else:
        return 'none'

def get_mcc_mnc():

    # Execute ADB command to get the MCC and MNC
    output = subprocess.check_output(['adb', 'shell', 'getprop', 'gsm.operator.numeric']).decode().strip()
    output = output.replace(",", "")

    # Split the output into MCC and MNC
    mcc = output[:3]
    mnc = output[3:]

    return mcc, mnc


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
    global connection_state, technology

    # Open file we created in write mode
    f = open(setUp(), "a")
    writer = csv.writer(f)

    while True:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = time.time()

        tech_index = 0  # Gives index of information about 2G, 3G, 4G or 5G when parsing some input
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
        output = subprocess.check_output(
            ['adb', 'shell', 'dumpsys', 'telephony.registry', '|', 'grep', 'mSignalStrength']).decode().strip()
        # print(output)

        network_type = get_network_type()
        print("Network type: " + network_type)
        try:
            # Connection to 4G
            if network_type == "4G":
                connection_state = "connectedRoaming"
                technology = "lte"

                signal_strength = output.split(',')[4].split(" ")  # Splitting ouput to get valuable information

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

                # Nedan gissar jag att dessa finns
                rssi = signal_strength[1].replace("rssi=", "")

            # No connection
            elif network_type == "none":
                # print(f"{timestamp}: Phone disconnected from 4G or 5G")
                connection_state = "Not Connected"
                technology = "none"
        except IndexError:
            print("IndexError: Could not read out network info at: " + timestamp)


        # Country and network code
        mcc, mnc = get_mcc_mnc()

        # write data to file
        input_line = [timestamp, apn1, apn2, connection_state, technology, raw_rssi, rssi, ber, rscp, rsrp, rsrq, mcc,
                      mnc,
                      network_provider, operator]
        writer.writerow(input_line)
        print(input_line)
        print()

        dt = time.time() - start_time
        time.sleep(10 - dt)  # for testing
        # time.sleep(10) # Ska logga var 10e sekund

    # i+=1 # for testing


## Run script ##
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted")
