#!/usr/bin/env python3

"""
===============================================================
Kea DHCP Automated Reservation Script
===============================================================

Purpose:
    This script automatically creates DHCP reservations in
    Kea DHCP using reservation information stored in a
    Google Sheet.

Data Flow:

    Google Sheet
         |
         v
    Published CSV
         |
         v
    Python Script
         |
         v
    Kea Control Agent API
         |
         v
    Kea DHCPv4
         |
         v
    DHCP Reservation

Google Sheet columns required:

    hostname, mac_address, reserved_ip

Example:

    client1,30:13:8B:C4:06:3D,192.168.10.151
    client2,00:15:5D:BB:2C:59,192.168.10.152
    client3,60:FF:9E:E3:02:7D,192.168.10.153

Why this script is used:
    Instead of manually adding every DHCP reservation in Kea,
    the administrator can maintain the reservation information
    in a Google Sheet.

    The script reads the sheet, validates the information,
    finds the correct Kea subnet, adds the reservations through
    the Kea Control Agent API, and verifies them.

===============================================================
"""

# ---------------------------------------------------------------
# IMPORT REQUIRED PYTHON LIBRARIES
# ---------------------------------------------------------------

import csv
import io
import ipaddress
import re
import requests


# ---------------------------------------------------------------
# GOOGLE SHEET CSV URL
# ---------------------------------------------------------------

# The Google Sheet is published as CSV.
#
# Why?
# Publishing the sheet as CSV allows the Python script to
# download the latest reservation information automatically
# without manually copying the data into the script.

CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQ2XMnB4-E5ec1nqEc_1uv7pV7BQKlG4MiTxfI6ZHh9Oj3dl3T1n5bYu67hX_zbHY23P071wh1Sgq1c/"
    "pub?output=csv"
)


# ---------------------------------------------------------------
# KEA CONTROL AGENT URL
# ---------------------------------------------------------------

# Kea Control Agent provides an HTTP API for communicating
# with Kea DHCP.
#
# Why?
# Instead of editing the Kea configuration file every time,
# the Python script can send commands directly to Kea through
# the Control Agent API.

KEA_URL = "http://127.0.0.1:8000/"


# ---------------------------------------------------------------
# HTTP HEADERS
# ---------------------------------------------------------------

# Kea Control Agent expects API requests in JSON format.
#
# Why?
# The Content-Type header tells Kea that the request body
# contains JSON data.

HEADERS = {
    "Content-Type": "application/json"
}


# ---------------------------------------------------------------
# MAC ADDRESS VALIDATION
# ---------------------------------------------------------------

# A valid MAC address contains six hexadecimal pairs.
#
# Example:
# 30:13:8B:C4:06:3D
#
# Why?
# Validation prevents an incorrectly formatted MAC address
# from being sent to Kea.

MAC_PATTERN = re.compile(
    r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$"
)


def validate_mac(mac):
    """
    Validate the MAC address.

    Why:
        Kea needs a valid hardware/MAC address to identify
        the DHCP client.
    """

    return bool(MAC_PATTERN.match(mac))


# ---------------------------------------------------------------
# IP ADDRESS VALIDATION
# ---------------------------------------------------------------

def validate_ip(ip):
    """
    Validate an IPv4 address.

    Why:
        The reserved IP must be a valid IP address before
        sending it to Kea.
    """

    try:
        address = ipaddress.ip_address(ip)

        # DHCP reservation in this project is IPv4.
        return address.version == 4

    except ValueError:
        return False


# ---------------------------------------------------------------
# DOWNLOAD GOOGLE SHEET DATA
# ---------------------------------------------------------------

def download_csv():
    """
    Download reservation data from the published Google Sheet.

    Why:
        This makes the Google Sheet the central location for
        maintaining DHCP reservation information.
    """

    print("[INFO] Downloading reservation data from Google Sheet...")

    response = requests.get(
        CSV_URL,
        timeout=20
    )

    # If the HTTP request failed, raise an error.
    #
    # Why:
    # Continuing with an unsuccessful download could result
    # in incorrect or empty reservation data.
    response.raise_for_status()

    print("[PASS] Google Sheet CSV downloaded successfully.")

    return response.text


# ---------------------------------------------------------------
# READ CSV DATA
# ---------------------------------------------------------------

def read_reservations(csv_text):
    """
    Read hostname, MAC address and reserved IP from CSV data.

    Why:
        The Python script needs to convert the CSV information
        into structured data before sending it to Kea.
    """

    reservations = []

    reader = csv.DictReader(
        io.StringIO(csv_text)
    )

    # Required columns in the Google Sheet.
    required_columns = {
        "hostname",
        "mac_address",
        "reserved_ip"
    }

    # Check whether all required columns exist.
    #
    # Why:
    # This prevents the script from running with an incorrectly
    # formatted Google Sheet.
    if not required_columns.issubset(reader.fieldnames or []):
        raise ValueError(
            "Google Sheet must contain: "
            "hostname, mac_address, reserved_ip"
        )

    for row in reader:

        # Remove unnecessary spaces from the values.
        hostname = row["hostname"].strip()
        mac_address = row["mac_address"].strip()
        reserved_ip = row["reserved_ip"].strip()

        # Ignore completely empty rows.
        if not hostname and not mac_address and not reserved_ip:
            continue

        reservations.append({
            "hostname": hostname,
            "mac_address": mac_address.lower(),
            "reserved_ip": reserved_ip
        })

    return reservations


# ---------------------------------------------------------------
# VALIDATE RESERVATION DATA
# ---------------------------------------------------------------

def validate_reservation(reservation):
    """
    Validate the MAC address and IP address.

    Why:
        Validation is performed before communicating with Kea.
        This reduces configuration errors and prevents invalid
        reservation requests.
    """

    hostname = reservation["hostname"]
    mac_address = reservation["mac_address"]
    reserved_ip = reservation["reserved_ip"]

    if not hostname:
        print("[FAIL] Hostname is empty.")
        return False

    if not validate_mac(mac_address):
        print(
            f"[FAIL] Invalid MAC address for {hostname}: "
            f"{mac_address}"
        )
        return False

    if not validate_ip(reserved_ip):
        print(
            f"[FAIL] Invalid IP address for {hostname}: "
            f"{reserved_ip}"
        )
        return False

    return True


# ---------------------------------------------------------------
# SEND REQUEST TO KEA CONTROL AGENT
# ---------------------------------------------------------------

def kea_request(payload):
    """
    Send a JSON request to the Kea Control Agent.

    Why:
        This is the main communication function between
        Python and Kea.

        Python
          |
          v
        HTTP POST
          |
          v
        Kea Control Agent
          |
          v
        Kea DHCPv4
    """

    response = requests.post(
        KEA_URL,
        headers=HEADERS,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------------
# FIND KEA DHCP SUBNET
# ---------------------------------------------------------------

def find_subnet_id(reserved_ip):
    """
    Find which Kea DHCP subnet contains the reserved IP.

    Why:
        Kea reservations belong to a specific subnet.
        Therefore, the script needs the correct subnet ID
        before adding the reservation.
    """

    payload = {
        "command": "subnet4-list",
        "service": ["dhcp4"]
    }

    result = kea_request(payload)

    # Extract the subnet information returned by Kea.
    arguments = result[0].get("arguments", {})

    subnets = arguments.get("subnets", [])

    target_ip = ipaddress.ip_address(reserved_ip)

    for subnet in subnets:

        subnet_network = ipaddress.ip_network(
            subnet["subnet"],
            strict=False
        )

        if target_ip in subnet_network:
            return subnet["id"]

    return None


# ---------------------------------------------------------------
# ADD RESERVATION TO KEA
# ---------------------------------------------------------------

def add_reservation(reservation, subnet_id):
    """
    Add a DHCP reservation to Kea.

    Why:
        This replaces manual reservation configuration.

        Example:

        MAC:
        30:13:8B:C4:06:3D

        Reserved IP:
        192.168.10.151

        The script sends this information directly to Kea.
    """

    payload = {
        "command": "reservation-add",
        "service": ["dhcp4"],
        "arguments": {
            "reservation": {
                "subnet-id": subnet_id,
                "hw-address": reservation["mac_address"],
                "ip-address": reservation["reserved_ip"],
                "hostname": reservation["hostname"]
            }
        }
    }

    return kea_request(payload)


# ---------------------------------------------------------------
# VERIFY RESERVATION
# ---------------------------------------------------------------

def verify_reservation(reservation, subnet_id):
    """
    Check whether the reservation exists in Kea.

    Why:
        Adding a reservation successfully is not enough.
        The script verifies that Kea actually contains the
        expected MAC-to-IP mapping.
    """

    payload = {
        "command": "reservation-get",
        "service": ["dhcp4"],
        "arguments": {
            "subnet-id": subnet_id,
            "identifier-type": "hw-address",
            "identifier": reservation["mac_address"]
        }
    }

    return kea_request(payload)


# ---------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------

def main():

    print()
    print("=" * 60)
    print(" KEA DHCP AUTOMATED RESERVATION")
    print("=" * 60)
    print()

    # -----------------------------------------------------------
    # STEP 1: DOWNLOAD GOOGLE SHEET
    # -----------------------------------------------------------

    try:
        csv_text = download_csv()

    except requests.RequestException as error:

        print("[FAIL] Could not download Google Sheet.")
        print(f"[ERROR] {error}")

        return


    # -----------------------------------------------------------
    # STEP 2: READ RESERVATION INFORMATION
    # -----------------------------------------------------------

    try:
        reservations = read_reservations(csv_text)

    except Exception as error:

        print("[FAIL] Could not read reservation data.")
        print(f"[ERROR] {error}")

        return


    print(
        f"[INFO] {len(reservations)} reservation(s) found."
    )

    print()


    # -----------------------------------------------------------
    # STEP 3: PROCESS EACH RESERVATION
    # -----------------------------------------------------------

    passed = 0
    failed = 0

    for reservation in reservations:

        hostname = reservation["hostname"]
        mac_address = reservation["mac_address"]
        reserved_ip = reservation["reserved_ip"]

        print("-" * 60)

        print(f"Hostname : {hostname}")
        print(f"MAC      : {mac_address}")
        print(f"IP       : {reserved_ip}")

        # -------------------------------------------------------
        # Validate reservation
        # -------------------------------------------------------

        if not validate_reservation(reservation):

            failed += 1
            continue


        # -------------------------------------------------------
        # Find subnet
        # -------------------------------------------------------

        try:

            subnet_id = find_subnet_id(
                reserved_ip
            )

        except Exception as error:

            print(
                f"[FAIL] Could not find Kea subnet: {error}"
            )

            failed += 1
            continue


        if subnet_id is None:

            print(
                f"[FAIL] No Kea subnet contains "
                f"{reserved_ip}"
            )

            failed += 1
            continue


        print(
            f"[INFO] Kea subnet ID: {subnet_id}"
        )


        # -------------------------------------------------------
        # Add reservation
        # -------------------------------------------------------

        try:

            add_result = add_reservation(
                reservation,
                subnet_id
            )

            print(
                f"[PASS] Reservation added for {hostname}"
            )

        except Exception as error:

            print(
                f"[FAIL] Could not add reservation: "
                f"{error}"
            )

            failed += 1
            continue


        # -------------------------------------------------------
        # Verify reservation
        # -------------------------------------------------------

        try:

            verify_result = verify_reservation(
                reservation,
                subnet_id
            )

            print(
                f"[PASS] Reservation verified for "
                f"{hostname}"
            )

            passed += 1

        except Exception as error:

            print(
                f"[FAIL] Reservation verification failed: "
                f"{error}"
            )

            failed += 1


    # -----------------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------------

    print()
    print("=" * 60)
    print(" FINAL RESULT")
    print("=" * 60)

    print(f"Successful reservations : {passed}")
    print(f"Failed reservations     : {failed}")

    print()

    if failed == 0:
        print("[SUCCESS] All DHCP reservations completed successfully.")
    else:
        print("[WARNING] Some reservations failed.")

    print()


# ---------------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------------

if __name__ == "__main__":

    # Why?
    # This ensures that main() runs only when this file is
    # executed directly using:
    #
    #     python3 kea_google_reservation.py
    #
    # It will not automatically run if this file is imported
    # into another Python program.

    main()