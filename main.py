"""
This is a Python script for logging the connection status of a Samsung phone
"""

import subprocess
from datetime import datetime
import time
import os
import csv


def create_directory():
    """ Set up a folder for logs"""
    # make folder if not exists
    current_working_directory = os.getcwd() + "/phone_log"
    if not os.path.exists(current_working_directory):
        os.makedirs(current_working_directory)


def create_new_log_file():
    """ Set up a new log file for each run"""
    # Some information for the file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    column_heads = ["timestamp", "apn1", "apn2", "connection_state", "technology", "raw_rssi", "rssi", "ber", "rscp",
                    "rsrp", "rsrq", "mcc", "mnc", "network_provider", "operator", "coordinates"]

    current_working_directory = os.getcwd() + "/phone_log"

    # make new file
    file_path = current_working_directory + "/connection_log_" + timestamp + ".csv"
    open(file_path, "x")  # Creates file
    file = open(file_path, "a")

    # Add column heads to file
    csv.writer(file).writerow(column_heads)
    file.close()

    return file_path


def get_gps_location():
    """ Find gps coordinates"""

    adb_command = "adb shell dumpsys location"
    output = subprocess.check_output(adb_command, shell=True, universal_newlines=True)

    # Split the output by lines and search for latitude and longitude
    for line in output.split('\n'):
        if 'last location' in line:
            pos = line.split(" ")[8]
            return pos


def get_mcc_mnc():
    """Get country code and operator code"""

    # Execute ADB command to get the MCC and MNC
    output = subprocess.check_output(['adb', 'shell', 'getprop', 'gsm.operator.numeric']).decode().strip()
    output = output.replace(",", "")

    # Split the output into MCC and MNC
    mcc = output[:3]
    mnc = output[3:]

    return mcc, mnc


def get_signal_data():
    """ Get data on signal strength and network type"""

    technology = ""
    rssi = "0"
    ber = "0"
    rscp = "0"
    rsrp = "0"
    rsrq = "0"
    connection_state = "Not Connected"

    network_type = subprocess.run(['adb', 'shell', 'getprop', 'gsm.network.type'],
                                  capture_output=True).stdout.decode().strip().lower()
    # print("Network type: " + network_type) # For testing

    signal_data = subprocess.check_output(
        ['adb', 'shell', 'dumpsys', 'telephony.registry', '|', 'grep', 'mSignalStrength']).decode().strip()
    # print("Signal strength: " + signal_data) # For more information when testing

    # Setting different parameters based on the type of network

    # Connection to 4G
    if 'lte' in network_type:
        connection_state = "connectedRoaming"
        technology = 'lte'

        signal_strength = signal_data.split(',')[4].split(
            " ")  # Splitting output to get valuable information. Magic number depends on network type

        rssi = signal_strength[1].replace("rssi=", "")
        rsrp = signal_strength[2].replace("rsrp=", "")
        rsrq = signal_strength[3].replace("rsrq=", "")

    # Connection to 3G
    elif "hspap" in network_type or 'umts' in network_type or 'wcdma' in network_type \
            or 'hsdpa' in network_type or 'hspa' in network_type or 'hsupa' in network_type:
        connection_state = "connectedRoaming"
        technology = network_type.replace(",unknown", "")

        signal_strength = signal_data.split(',')[2].split(" ")  # Splitting output to get valuable information

        rscp = signal_strength[3].replace("rscp=", "")
        ber = signal_strength[2].replace("ber=", "")

    # Connection to 2G
    elif 'edge' in network_type:
        connection_state = "connectedRoaming"
        technology = 'edge'
        signal_strength = signal_data.split(',')[1].split(" ")  # Splitting output to get valuable information

        rssi = signal_strength[1].replace("rssi=", "")
        ber = signal_strength[2].replace("ber=", "")

    # Connection to 5G. Currently network type is always LTE both when connected to 4G and 5G.
    elif 'nr' in network_type:
        connection_state = "connectedRoaming"
        technology = 'nr'
        signal_strength = signal_data.split(',')[5].split(" ")  # Splitting ouput to get valuable information

        # Nedan gissar jag att dessa finns
        rssi = signal_strength[1].replace("rssi=", "")

    # No connection
    elif network_type == "none":
        technology = "none"

    return connection_state, technology, rssi, rsrp, rsrq, rscp, ber


def main():
    """ Main Method """

    # Open file we created in write mode
    create_directory()
    file = open(create_new_log_file(), "a")

    writer = csv.writer(file)

    while True:
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

        # GPS position
        pos = get_gps_location()

        # Write to csv file
        input_line = [timestamp, apn1, apn2, connection_state, technology, raw_rssi, rssi, ber, rscp, rsrp, rsrq, mcc,
                      mnc, network_provider, operator, pos]
        writer.writerow(input_line)

        print(input_line, "\n")

        dt = time.time() - start_time  # Adjusting time sleeping so it's always exactly 10 seconds
        time.sleep(10 - dt)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted")
    except subprocess.CalledProcessError:
        print(
            "\n Error: No device found \n Make sure you have: \n 1. Enabled USB debugging in Developer options \n 2. "
            "Allowed usb debugging on the screen when plugging in the usb. Remove the usb and plug in again if this "
            "pop-up doesn't show up. \n 2. Changed 'USB charging' to 'File transfer' \n \n Script interrupted.")
    except IndexError:
        print(
            "Error: \n GPS location is not turned on. Go to Google maps, and try to navigate from 'your location' to "
            "allow GPS use. \n \n Script interrupted.")
