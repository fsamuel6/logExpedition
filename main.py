# This is a Python script for logging the connection status of a Samsung phone

import subprocess
from datetime import datetime
import time
import os
import csv
import geocoder

## Set up a folder and a new log file for each run
def setUp():
    # Some information for the file
    time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    column_heads = ["timestamp", "apn1", "apn2", "connection_state", "technology", "raw_rssi", "rssi", "ber", "rscp",
                    "rsrp", "rsrq", "mcc", "mnc", "network_provider", "operator", "coordinates"]

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



def get_mcc_mnc():

    # Execute ADB command to get the MCC and MNC
    output = subprocess.check_output(['adb', 'shell', 'getprop', 'gsm.operator.numeric']).decode().strip()
    output = output.replace(",", "")

    # Split the output into MCC and MNC
    mcc = output[:3]
    mnc = output[3:]

    return mcc, mnc



def get_signal_data():
    technology = ""
    rssi = "0"
    ber = "0"
    rscp = "0"
    rsrp = "0"
    rsrq = "0"
    connection_state = "Not Connected"

    network_type = subprocess.run(['adb', 'shell', 'getprop', 'gsm.network.type'], capture_output=True).stdout.decode().strip().lower()
    print("Network connection: " + network_type)

    signal_data = subprocess.check_output(
        ['adb', 'shell', 'dumpsys', 'telephony.registry', '|', 'grep', 'mSignalStrength']).decode().strip()

    # Connection to 4G
    if 'lte' in network_type:
        connection_state = "connectedRoaming"
        technology = 'lte'

        signal_strength = signal_data.split(',')[4].split(" ")  # Splitting ouput to get valuable information

        rssi = signal_strength[1].replace("rssi=", "")
        rsrp = signal_strength[2].replace("rsrp=", "")
        rsrq = signal_strength[3].replace("rsrq=", "")

    # Connection to 3G
    elif "hspap" in network_type or 'umts' in network_type or 'wcdma' in network_type or 'hsdpa' in network_type or 'hspa' in network_type or 'hsupa' in network_type:
        connection_state = "connectedRoaming"
        technology = network_type.replace(",unknown", "")
        signal_strength = signal_data.split(',')[2].split(" ")  # Splitting ouput to get valuable information
        rscp = signal_strength[3].replace("rscp=", "")
        ber = signal_strength[2].replace("ber=", "")

    # Connection to 2G
    elif 'edge' in network_type:
        connection_state = "connectedRoaming"
        technology = 'edge'
        signal_strength = signal_data.split(',')[1].split(" ")  # Splitting ouput to get valuable information
        rssi = signal_strength[1].replace("rssi=", "")
        ber = signal_strength[2].replace("ber=", "")

    # Connection to 5G
    elif 'nr' in network_type:
        connection_state = "connectedRoaming"
        technology = 'nr'
        signal_strength = signal_data.split(',')[5].split(" ")  # Splitting ouput to get valuable information

        # Nedan gissar jag att dessa finns
        rssi = signal_strength[1].replace("rssi=", "")

    # No connection
    elif network_type == "none":
        # print(f"{timestamp}: Phone disconnected from 4G or 5G")

        technology = "none"

    return connection_state, technology, rssi, rsrp, rsrq, rscp, ber


## Main method ##
def main():

    # Open file we created in write mode
    f = open(setUp(), "a")
    writer = csv.writer(f)

    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            start_time = time.time()

            apn1 = "0"
            apn2 = "0"
            raw_rssi = "0"

            network_provider = ""
            operator = ""

            # Data on type of network and signal strength
            connection_state, technology, rssi, rsrp, rsrq, rscp, ber = get_signal_data()

            # Country and network code
            mcc, mnc = get_mcc_mnc()

            # Coordinates
            g = geocoder.ip('me')

            coordinates = g.latlng
            print(coordinates)

            # write data to file
            input_line = [timestamp, apn1, apn2, connection_state, technology, raw_rssi, rssi, ber, rscp, rsrp, rsrq, mcc,
                          mnc, network_provider, operator, str(coordinates[0]) + "," + str(coordinates[1])]
            writer.writerow(input_line)

            print(input_line)
            print()

            dt = time.time() - start_time
            time.sleep(10 - dt)
        except IndexError:
            print("IndexError: Could not read out network info at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



## Run script ##
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted")
