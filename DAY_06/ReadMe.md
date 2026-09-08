# Day 6 – Kea DHCP Migration and Automated DHCP Reservation

## Overview

On Day 5, the existing DHCP implementation was further developed based on a new technical requirement. The DHCP service was migrated from **ISC DHCP to Kea DHCP**, followed by the implementation of an automated DHCP reservation system.

The work was completed in two phases:

1. **Migration to Kea DHCP**
2. **Automated DHCP Reservation using Google Sheets and Python**

The final implementation connects a Google Sheet with the Kea DHCP server through a Python automation script and the Kea Control Agent API.

---

## 1. Migration to Kea DHCP

### Objective

The first objective was to replace the previously configured ISC DHCP server with **Kea DHCPv4** and verify that the new DHCP server could successfully provide IP addresses to clients.

### Implementation

The following activities were completed:

* Installed Kea DHCP on the Linux server.
* Configured Kea DHCPv4.
* Configured the required DHCP subnet and IP address pool.
* Configured network parameters such as subnet mask, gateway, DNS, and lease settings.
* Validated the Kea DHCP configuration.
* Started and verified the Kea DHCPv4 service.
* Tested DHCP address allocation using a client.

### DHCP Testing

The DHCP client was configured to obtain an IP address automatically.

The client successfully communicated with the Kea DHCP server and received an IP address from the configured DHCP pool.

**Result: PASS**

Kea DHCPv4 was successfully installed, configured, and tested.

---

# 2. Kea Control Agent

The next stage was to configure the **Kea Control Agent**.

The Control Agent provides an API interface that allows external applications to communicate with Kea DHCP. This API was required for implementing automated DHCP reservations.

### Activities Completed

* Configured the Kea Control Agent.
* Started the Control Agent service.
* Tested API communication.
* Verified that requests could be sent to the Kea DHCP service.

**Result: PASS**

Communication between the Python automation environment and the Kea Control Agent was successfully established.

---

# 3. DHCP Reservation Using Kea

After testing the basic Kea DHCP functionality, a DHCP reservation was configured.

A DHCP reservation associates a client's MAC address with a specific IP address. When the client requests an IP address, Kea identifies the client using its MAC address and provides the configured reserved IP.

The reservation was added through the Kea Control Agent API and subsequently verified.

**Result: PASS**

The DHCP reservation was successfully created and verified in Kea.

---

# 4. Automated DHCP Reservation

## Objective

The next enhancement was to automate the DHCP reservation process.

Instead of manually editing the Kea configuration whenever a reservation was required, a **Google Sheet** was used as a centralized reservation database.

A Python script was developed to retrieve the reservation information and automatically configure Kea through the Control Agent API.

---

## 5. System Architecture

The final system follows this workflow:

```text
                 Google Sheet
                      │
                      ▼
                Published CSV
                      │
                      ▼
             Python Automation
                      │
                      ▼
          Kea Control Agent API
                      │
                      ▼
                Kea DHCPv4
                      │
                      ▼
                 DHCP Client
                      │
                      ▼
             Reserved IP Address
```

---

# 6. Google Sheet Configuration

The Google Sheet contains the DHCP reservation information using three fields:

| Field         | Description                        |
| ------------- | ---------------------------------- |
| `hostname`    | Name assigned to the client        |
| `mac_address` | MAC address of the DHCP client     |
| `reserved_ip` | IP address reserved for the client |

### Example Data

| Hostname | MAC Address         | Reserved IP      |
| -------- | ------------------- | ---------------- |
| client1  | `30:13:8B:C4:06:3D` | `192.168.10.151` |
| client2  | `00:15:5D:BB:2C:59` | `192.168.10.152` |
| client3  | `60:FF:9E:E3:02:7D` | `192.168.10.153` |

The Google Sheet was published as a CSV file so that it could be accessed programmatically by the Python script.

---

# 7. Python Automation

A Python script was developed to automate the complete reservation process.

### Python Automation Workflow

The script performs the following operations:

1. Downloads the published Google Sheet CSV.
2. Reads the reservation data.
3. Extracts the hostname, MAC address, and reserved IP.
4. Validates the reservation information.
5. Communicates with the Kea Control Agent.
6. Retrieves the configured DHCPv4 subnet information.
7. Identifies the appropriate subnet for the reserved IP.
8. Sends a `reservation-add` request to Kea.
9. Creates the DHCP reservation.
10. Verifies the reservation through the Kea API.
11. Reports the result of the operation.

This eliminates the need to manually edit DHCP reservation configuration for every client.

---

# 8. Automation Testing

The automation was tested step by step.

### Test 1 – Google Sheet to CSV

The published Google Sheet was accessed from the Linux server using the CSV endpoint.

The reservation data was successfully retrieved.

**Result: PASS**

---

### Test 2 – Python Data Processing

The Python script successfully downloaded and processed the CSV data.

The following information was correctly extracted:

```text
client1 → 30:13:8B:C4:06:3D → 192.168.10.151
client2 → 00:15:5D:BB:2C:59 → 192.168.10.152
client3 → 60:FF:9E:E3:02:7D → 192.168.10.153
```

**Result: PASS**

---

### Test 3 – Python to Kea Control Agent

The Python script successfully communicated with the Kea Control Agent API.

**Result: PASS**

---

### Test 4 – Automatic Reservation Creation

The Python script sent reservation requests to Kea using the client's MAC address and reserved IP address.

The reservations were successfully added to Kea.

**Result: PASS**

---

### Test 5 – Reservation Verification

The created reservations were queried through the Kea API.

The configured MAC addresses and reserved IP addresses were successfully verified.

**Result: PASS**

---

### Test 6 – DHCP Client Test

The DHCP client's existing lease was released and a new DHCP request was made.

Kea identified the client's MAC address and matched it with the configured reservation.

The client successfully received its reserved IP address.

Example:

```text
MAC Address : 30:13:8B:C4:06:3D
Reserved IP : 192.168.10.151
```

**Result: PASS**

---

# 9. End-to-End Test

The complete automation pipeline was successfully tested:

```text
Google Sheet
     │
     ▼
Published CSV
     │
     ▼
Python Script
     │
     ▼
Kea Control Agent API
     │
     ▼
DHCP Reservation
     │
     ▼
Kea DHCPv4
     │
     ▼
DHCP Client
     │
     ▼
Reserved IP Received
```

### Final Test Results

| Test                       | Status |
| -------------------------- | ------ |
| Kea DHCP installation      | ✅ PASS |
| Kea DHCP configuration     | ✅ PASS |
| DHCP address allocation    | ✅ PASS |
| Kea Control Agent          | ✅ PASS |
| Kea API communication      | ✅ PASS |
| DHCP reservation           | ✅ PASS |
| Google Sheet CSV retrieval | ✅ PASS |
| Python automation          | ✅ PASS |
| Reservation verification   | ✅ PASS |
| DHCP client test           | ✅ PASS |
| End-to-end automation      | ✅ PASS |

---

# 10. ISC DHCP vs Automated Kea DHCP

The implementation evolved from a manually managed DHCP reservation system to an API-driven automated solution.

| Feature                      | ISC DHCP                        | Kea + Automation      |
| ---------------------------- | ------------------------------- | --------------------- |
| DHCP service                 | ISC DHCP                        | Kea DHCPv4            |
| IP allocation                | Manual configuration            | Configured DHCP pool  |
| Reservation                  | Manual                          | Automated             |
| Reservation source           | DHCP configuration              | Google Sheet          |
| Update method                | Edit configuration              | Update Google Sheet   |
| API integration              | Not used in this implementation | Kea Control Agent API |
| Python automation            | Not used                        | Implemented           |
| Centralized reservation data | No                              | Yes                   |
| Automated reservation        | No                              | Yes                   |

---

# 11. Benefits of the Automated Approach

The automated Kea implementation provides several improvements:

* Reduces manual DHCP configuration.
* Provides a centralized location for reservation information.
* Allows reservation data to be maintained through a spreadsheet.
* Uses Python to automate repetitive configuration tasks.
* Uses the Kea Control Agent API for dynamic reservation management.
* Makes it easier to add or update multiple client reservations.
* Reduces the possibility of manual configuration errors.
* Provides a foundation for further DHCP automation.

---

# 12. Final Outcome

The Day 5 task was successfully completed.

The DHCP environment was migrated from ISC DHCP to Kea DHCPv4, and the Kea Control Agent was configured and tested.

The DHCP reservation process was then automated using:

* **Google Sheets** for reservation data
* **Published CSV** for data access
* **Python** for automation
* **Kea Control Agent API** for DHCP management
* **Kea DHCPv4** for IP address allocation

The complete system was tested successfully from the Google Sheet through to the DHCP client.

The client successfully received the IP address associated with its MAC address.

## Final Status

**✅ COMPLETED**

**✅ DHCP SERVER TESTED**

**✅ KEA API TESTED**

**✅ AUTOMATED RESERVATION TESTED**

**✅ DHCP CLIENT VERIFIED**

**✅ END-TO-END TEST PASSED**

---

## 13. Key Learning Outcomes

Through this task, the following technical areas were practiced:

* Linux DHCP server administration
* ISC DHCP configuration
* Kea DHCPv4 configuration
* DHCP reservation management
* DHCP client-server communication
* REST/API-based server management
* Kea Control Agent
* Python automation
* CSV data processing
* Google Sheets integration
* Network troubleshooting and testing

---

## Conclusion

This task progressed from a basic DHCP implementation to an automated DHCP reservation management system.

The initial implementation used ISC DHCP with manually configured reservations. Following the introduction of a new requirement, the environment was migrated to Kea DHCPv4. The reservation process was subsequently enhanced by integrating Google Sheets, Python, and the Kea Control Agent API.

The final implementation successfully demonstrated an automated workflow in which reservation information stored in Google Sheets was retrieved by Python, sent to Kea through its API, and used by Kea DHCP to provide the correct reserved IP address to the client.
