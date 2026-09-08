
# Day 6 – Kea DHCP Configuration and Automated Reservation

## 1. Objective

The objective of Day 6 was to implement **Kea DHCPv4** and automate DHCP reservations using:

```text
Google Sheet
     ↓
Published CSV
     ↓
Python Automation Script
     ↓
Kea Control Agent API
     ↓
Kea DHCPv4
     ↓
DHCP Client
     ↓
Reserved IP Address
```

The main activities were:

* Install Kea DHCPv4
* Configure Kea DHCP
* Validate the configuration
* Start and test the Kea DHCP service
* Configure Kea Control Agent
* Test the Control Agent API
* Create DHCP reservations
* Automate reservations using Python
* Read reservation details from Google Sheets
* Verify reservations through Kea API
* Test the DHCP client

---

# 2. Update Ubuntu Packages

```bash
sudo apt update
```

This updates the Ubuntu package information before installing Kea.

---

# 3. Install Kea DHCPv4

```bash
sudo apt install kea-dhcp4-server -y
```

This installs the Kea DHCPv4 server.

Check the installation:

```bash
kea-dhcp4 -V
```

---

# 4. Check Kea DHCP Service

```bash
sudo systemctl status kea-dhcp4-server
```

Start the service:

```bash
sudo systemctl start kea-dhcp4-server
```

Enable the service at system startup:

```bash
sudo systemctl enable kea-dhcp4-server
```

Restart the service after configuration changes:

```bash
sudo systemctl restart kea-dhcp4-server
```

---

# 5. Configure Kea DHCPv4

Open the Kea DHCP configuration:

```bash
sudo nano /etc/kea/kea-dhcp4.conf
```

The configuration contains the DHCP network information, address pool, gateway, DNS server, and lease database.

Example network:

```text
Subnet:       192.168.10.0/24
DHCP Pool:    192.168.10.100 - 192.168.10.200
Gateway:      192.168.10.1
DNS:          8.8.8.8
```

After saving the configuration, validate it.

---

# 6. Validate Kea Configuration

```bash
sudo kea-dhcp4 -t -c /etc/kea/kea-dhcp4.conf
```

This checks the Kea configuration for syntax and configuration errors before restarting the service.

Restart Kea:

```bash
sudo systemctl restart kea-dhcp4-server
```

Check the status:

```bash
sudo systemctl status kea-dhcp4-server
```

---

# 7. Check Kea DHCP Logs

```bash
sudo journalctl -u kea-dhcp4-server --no-pager -n 50
```

This command was used to check whether Kea started correctly and to identify any DHCP configuration or runtime errors.

---

# 8. Configure Kea Control Agent

The **Kea Control Agent** provides an HTTP API that allows Kea DHCP to be managed dynamically.

Check the service:

```bash
sudo systemctl status kea-ctrl-agent
```

Start the service:

```bash
sudo systemctl start kea-ctrl-agent
```

Enable it:

```bash
sudo systemctl enable kea-ctrl-agent
```

Restart it when required:

```bash
sudo systemctl restart kea-ctrl-agent
```

Check the logs:

```bash
sudo journalctl -u kea-ctrl-agent --no-pager -n 50
```

---

# 9. Check Kea Control Agent Port

```bash
sudo ss -lntp
```

The Control Agent was configured to listen on:

```text
127.0.0.1:8000
```

---

# 10. Test Kea Control Agent API

The Control Agent API was tested using `curl`.

```bash
curl -s -X POST http://127.0.0.1:8000/ \
-H "Content-Type: application/json" \
-d '{
    "command": "list-commands",
    "service": ["dhcp4"]
}'
```

A successful response confirmed communication between:

```text
curl
 ↓
Kea Control Agent
 ↓
Kea DHCPv4
```

---

# 11. Install Python Requests Library

The automation script communicates with the Kea Control Agent API using Python.

Install the required Python package:

```bash
sudo apt install python3-requests -y
```

Verify Python:

```bash
python3 --version
```

---

# 12. Test Google Sheet CSV

The DHCP reservation information was maintained in a Google Sheet with:

```text
hostname,mac_address,reserved_ip
```

The Google Sheet was published as a CSV file.

Test the published CSV:

```bash
curl -L "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2XMnB4-E5ec1nqEc_1uv7pV7BQKlG4MiTxfI6ZHh9Oj3dl3T1n5bYu67hX_zbHY23P071wh1Sgq1c/pub?output=csv"
```

Example data:

```text
hostname,mac_address,reserved_ip
client1,30:13:8B:C4:06:3D,192.168.10.151
client2,00:15:5D:BB:2C:59,192.168.10.152
client3,60:FF:9E:E3:02:7D,192.168.10.153
```

This confirmed that the Google Sheet could be accessed programmatically.

---

# 13. Create Python Automation Script

Create the Python script:

```bash
nano ~/kea_google_reservation.py
```

The script performs the following operations:

```text
1. Download Google Sheet CSV
2. Read hostname, MAC address and reserved IP
3. Validate MAC address
4. Validate IP address
5. Connect to Kea Control Agent
6. Discover the Kea DHCP subnet
7. Add the reservation using Kea API
8. Verify the reservation
9. Display PASS/FAIL result
```

---

# 14. Run the Automation Script

```bash
python3 ~/kea_google_reservation.py
```

The script automatically reads the reservation information from Google Sheets and sends it to Kea through the Control Agent API.

The process becomes:

```text
Google Sheet
     ↓
CSV
     ↓
Python Script
     ↓
Kea Control Agent
     ↓
reservation-add
     ↓
Kea DHCP
```

---

# 15. Add Reservation Through Kea API

A reservation can also be tested directly using the Kea Control Agent:

```bash
curl -s -X POST http://127.0.0.1:8000/ \
-H "Content-Type: application/json" \
-d '{
    "command": "reservation-add",
    "service": ["dhcp4"],
    "arguments": {
        "reservation": {
            "subnet-id": 1,
            "hw-address": "30:13:8b:c4:06:3d",
            "ip-address": "192.168.10.151",
            "hostname": "client1"
        }
    }
}'
```

This associates:

```text
MAC Address → Reserved IP

30:13:8b:c4:06:3d → 192.168.10.151
```

---

# 16. Verify Reservation

The reservation was checked using:

```bash
curl -s -X POST http://127.0.0.1:8000/ \
-H "Content-Type: application/json" \
-d '{
    "command": "reservation-get",
    "service": ["dhcp4"],
    "arguments": {
        "subnet-id": 1,
        "identifier-type": "hw-address",
        "identifier": "30:13:8b:c4:06:3d"
    }
}'
```

The response was checked to confirm that the MAC address was associated with the correct reserved IP.

---

# 17. Test DHCP Client

On the DHCP client, release the existing lease:

```bash
sudo dhclient -r
```

Request a new DHCP address:

```bash
sudo dhclient -v
```

Check the assigned IP:

```bash
ip addr
```

The DHCP client successfully received the configured reserved IP:

```text
192.168.10.151
```

---

# 18. Check DHCP Lease Database

```bash
sudo cat /var/lib/kea/kea-leases4.csv
```

This can be used to check the DHCP leases maintained by Kea.

---

# 19. Final Service Verification

Check Kea DHCP:

```bash
sudo systemctl status kea-dhcp4-server
```

Check Control Agent:

```bash
sudo systemctl status kea-ctrl-agent
```

Check listening ports:

```bash
sudo ss -lntp
```

Check DHCP logs:

```bash
sudo journalctl -u kea-dhcp4-server --no-pager -n 50
```

Check Control Agent logs:

```bash
sudo journalctl -u kea-ctrl-agent --no-pager -n 50
```

---

# 20. Testing Results

| Test                      | Result |
| ------------------------- | ------ |
| Kea DHCPv4 installation   | ✅ PASS |
| Kea DHCP configuration    | ✅ PASS |
| Configuration validation  | ✅ PASS |
| Kea DHCP service          | ✅ PASS |
| Kea Control Agent         | ✅ PASS |
| Control Agent API         | ✅ PASS |
| Google Sheet CSV access   | ✅ PASS |
| Python automation         | ✅ PASS |
| DHCP reservation addition | ✅ PASS |
| Reservation verification  | ✅ PASS |
| DHCP client testing       | ✅ PASS |
| Reserved IP assignment    | ✅ PASS |

---

# 21. Final Architecture

```text
             Google Sheet
                  │
                  │ Published CSV
                  ↓
        Python Automation Script
                  │
                  │ HTTP API
                  ↓
        Kea Control Agent :8000
                  │
                  ↓
             Kea DHCPv4
                  │
                  │ DHCP
                  ↓
            DHCP Client
                  │
                  ↓
          Reserved IP Address
             192.168.10.151
```

# 22. Conclusion

Day 6 successfully completed the **Kea DHCP server implementation and automated DHCP reservation system**.

Kea DHCPv4 was installed, configured, validated, and tested. The Kea Control Agent was configured and its API was verified. A Python automation script was then developed to retrieve DHCP reservation information from a Google Sheet and automatically configure the reservations in Kea.

The final DHCP client test successfully received the reserved IP address, confirming that the complete automation workflow was working correctly.

**Day 6 Status: COMPLETED SUCCESSFULLY ✅**
