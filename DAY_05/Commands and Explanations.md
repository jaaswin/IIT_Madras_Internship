# DHCP Server Task – Commands and Explanations

## 1. Check Network Interface

### Command

```bash
ip addr
```

### Explanation

Displays the network interfaces available on the Linux system and their IP addresses.

### Why I used it

I used this command to identify the network interface connected to the network and check its current IP address.

### What to check

Look for interfaces such as:

```text
eth0
ens33
enp0s3
```

and their IPv4 addresses.

---

## 2. Check Network Interfaces

### Command

```bash
ip link
```

### Explanation

Shows all network interfaces and whether they are **UP** or **DOWN**.

### Why I used it

I used it to verify that the required network interface was active before configuring the DHCP server.

---

## 3. Check Routing Table

### Command

```bash
ip route
```

### Explanation

Displays the Linux routing table.

### Why I used it

I used it to understand how the Linux system communicates with other networks and to check the default gateway.

Example:

```text
default via 192.168.10.1 dev eth0
```

---

# DHCP Server Installation

## 4. Update Package Information

### Command

```bash
sudo apt update
```

### Explanation

Updates the list of available software packages from the configured Ubuntu repositories.

### Why I used it

Before installing the DHCP server, I updated the package information to make sure Ubuntu had the latest available package information.

### Important

`apt update` does **not** install or upgrade the software. It only updates the package list.

---

## 5. Install DHCP Server

### Command

```bash
sudo apt install isc-dhcp-server
```

### Explanation

Installs the **ISC DHCP server** package on Ubuntu/Linux.

### Why I used it

This was the main installation command for setting up the Linux machine as a DHCP server.

### Result

After successful installation, the DHCP server configuration files and service become available.

---

## 6. Verify DHCP Package Installation

### Command

```bash
dpkg -l | grep isc-dhcp-server
```

### Explanation

Checks the installed Debian/Ubuntu packages and searches for the ISC DHCP server package.

### Why I used it

I used it to verify that the DHCP server package was successfully installed.

---

# DHCP Service Management

## 7. Check DHCP Service Status

### Command

```bash
sudo systemctl status isc-dhcp-server
```

### Explanation

Displays the current status of the DHCP server service.

### Why I used it

I used this command to check whether the DHCP server was running correctly.

### Possible result

```text
Active: active (running)
```

This indicates that the service is running.

---

## 8. Start DHCP Server

### Command

```bash
sudo systemctl start isc-dhcp-server
```

### Explanation

Starts the DHCP server service.

### Why I used it

I used this command when the DHCP service was not already running.

---

## 9. Restart DHCP Server

### Command

```bash
sudo systemctl restart isc-dhcp-server
```

### Explanation

Stops and starts the DHCP service again.

### Why I used it

I used it after modifying the DHCP configuration so that the server would load the new configuration.

### Example

After changing:

```text
/etc/dhcp/dhcpd.conf
```

I restarted the DHCP service.

---

## 10. Enable DHCP Server at Boot

### Command

```bash
sudo systemctl enable isc-dhcp-server
```

### Explanation

Configures the DHCP service to start automatically when Linux boots.

### Why I used it

This makes the DHCP server automatically start after a system restart.

---

# DHCP Configuration

## 11. Open DHCP Configuration File

### Command

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

### Explanation

Opens the main ISC DHCP server configuration file using the Nano text editor.

### Why I used it

I used this file to configure:

* DHCP network
* IP address range
* Subnet mask
* Gateway
* DNS servers
* Lease time
* DHCP reservation

---

# 12. Configure DHCP Options

### Configuration

```conf
option domain-name-servers 8.8.8.8, 1.1.1.1;

default-lease-time 600;
max-lease-time 7200;

authoritative;
```

### Explanation

#### DNS servers

```conf
option domain-name-servers 8.8.8.8, 1.1.1.1;
```

Provides DNS server addresses to DHCP clients.

* `8.8.8.8` = Google DNS
* `1.1.1.1` = Cloudflare DNS

#### Default lease time

```conf
default-lease-time 600;
```

The normal DHCP lease duration is **600 seconds**, or 10 minutes.

#### Maximum lease time

```conf
max-lease-time 7200;
```

The maximum lease duration is **7200 seconds**, or 2 hours.

#### Authoritative

```conf
authoritative;
```

Indicates that this DHCP server is the authoritative DHCP server for the configured network.

---

# 13. Configure DHCP Network

### Configuration

```conf
subnet 192.168.10.0 netmask 255.255.255.0 {
    range 192.168.10.100 192.168.10.200;
    option subnet-mask 255.255.255.0;
    option routers 192.168.10.1;
    option domain-name-servers 8.8.8.8, 1.1.1.1;
}
```

### Explanation

### Subnet

```conf
subnet 192.168.10.0
```

Defines the network address.

### Netmask

```conf
netmask 255.255.255.0
```

Defines the subnet mask.

This is equivalent to:

```text
/24
```

### DHCP Range

```conf
range 192.168.10.100 192.168.10.200;
```

Defines the range of IP addresses that DHCP can automatically assign to clients.

So the DHCP server can provide addresses from:

```text
192.168.10.100
        ↓
192.168.10.200
```

### Router

```conf
option routers 192.168.10.1;
```

Provides the default gateway to DHCP clients.

### DNS

```conf
option domain-name-servers 8.8.8.8, 1.1.1.1;
```

Provides DNS servers to the client.

---

# Configuration Testing

## 14. Test DHCP Configuration Syntax

### Command

```bash
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf
```

### Explanation

Checks the DHCP configuration file for syntax errors.

### Why I used it

I used this command before restarting the DHCP service to make sure that the configuration was written correctly.

### If successful

There should be no major syntax error reported.

### Why this is important

If the configuration contains an error, the DHCP service may fail to start.

---

# DHCP Client Testing

After configuring the DHCP server, I connected the **DHCP server and laptop through a network switch**.

The laptop was configured to obtain its IP address automatically.

---

# 15. Check Laptop IP Address

On Windows PowerShell or Command Prompt:

```powershell
ipconfig
```

### Explanation

Displays the IP address configuration of the Windows laptop.

### Why I used it

I used it to check whether the laptop successfully received an IP address from the DHCP server.

### Expected result

The laptop should receive an address from the configured DHCP range.

For example:

```text
IPv4 Address : 192.168.10.100
```

---

# 16. View Detailed IP Information

### Command

```powershell
ipconfig /all
```

### Explanation

Displays detailed network configuration.

It shows:

* IPv4 address
* IPv6 address
* Subnet mask
* Default gateway
* DNS servers
* DHCP enabled status
* MAC/physical address
* DHCP server address

### Why I used it

I used this command to verify that the laptop was receiving its network configuration from the DHCP server.

---

# 17. Release DHCP Address

### Command

```powershell
ipconfig /release
```

### Explanation

Releases the current DHCP-assigned IP address.

### Why I used it

I used this during DHCP testing to remove the current lease from the laptop.

After releasing the address, the laptop no longer uses that DHCP address.

---

# 18. Request a New DHCP Address

### Command

```powershell
ipconfig /renew
```

### Explanation

Requests a new IP address from the DHCP server.

### Why I used it

I used this to test whether the DHCP server could successfully provide an IP address to the laptop.

### Testing flow

```text
ipconfig /release
        ↓
ipconfig /renew
        ↓
ipconfig
```

The final `ipconfig` was used to verify the newly assigned address.

---

# DHCP Reservation

## 19. Find Laptop MAC Address

### Command

```powershell
getmac
```

### Explanation

Displays the physical/MAC addresses of the network adapters.

### Why I used it

DHCP reservation requires the client's MAC address.

The DHCP server uses the MAC address to identify a particular device.

---

## 20. Get Detailed MAC Address

### Command

```powershell
ipconfig /all
```

Look for:

```text
Physical Address
```

Example:

```text
Physical Address : AA-BB-CC-DD-EE-FF
```

This is the laptop's MAC address.

---

# 21. Configure DHCP Reservation

I opened the DHCP configuration file again:

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Then added a reservation similar to:

```conf
host laptop {
    hardware ethernet AA:BB:CC:DD:EE:FF;
    fixed-address 192.168.10.50;
}
```

### Explanation

```conf
host laptop
```

Creates a DHCP host definition for the laptop.

```conf
hardware ethernet AA:BB:CC:DD:EE:FF;
```

Specifies the laptop's MAC address.

```conf
fixed-address 192.168.10.50;
```

Assigns a fixed IP address to that particular laptop.

### Why I used it

The purpose of DHCP reservation was to make sure that the same laptop receives the same IP address whenever it requests an address from the DHCP server.

---

# 22. Test Configuration Again

### Command

```bash
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf
```

### Why I used it

After adding the reservation, I checked the configuration again before restarting the DHCP server.

This helps detect configuration mistakes.

---

# 23. Restart DHCP Server

### Command

```bash
sudo systemctl restart isc-dhcp-server
```

### Why I used it

The DHCP server needs to reload the modified configuration containing the reservation.

---

# 24. Check DHCP Service Again

### Command

```bash
sudo systemctl status isc-dhcp-server
```

### Why I used it

I verified that the DHCP server was running successfully after adding the reservation.

---

# 25. Renew Laptop IP

On Windows:

```powershell
ipconfig /release
```

Then:

```powershell
ipconfig /renew
```

Finally:

```powershell
ipconfig
```

### Why I used it

This forced the laptop to request a DHCP address again.

I then checked whether the laptop received the **reserved IP address**.

---

# DHCP Logs

## 26. View DHCP Logs

### Command

```bash
sudo journalctl -u isc-dhcp-server
```

### Explanation

Displays system logs related to the ISC DHCP server.

### Why I used it

I used the logs to verify DHCP activity and troubleshoot problems if the client did not receive an IP address.

---

## 27. View Recent DHCP Logs

### Command

```bash
sudo journalctl -u isc-dhcp-server -n 50
```

### Explanation

Displays the latest 50 DHCP service log entries.

### Why I used it

It is easier to check recent DHCP events instead of viewing the complete log history.

---

## 28. Monitor DHCP Logs Live

### Command

```bash
sudo journalctl -u isc-dhcp-server -f
```

### Explanation

Continuously displays new DHCP log entries as they occur.

### Why I used it

During testing, this can be used to observe DHCP requests and responses in real time.

---

# DHCP Lease Information

## 29. Check DHCP Lease File

### Command

```bash
sudo cat /var/lib/dhcp/dhcpd.leases
```

### Explanation

Displays the DHCP leases recorded by the DHCP server.

### Why I used it

I used it to check which IP addresses were leased to DHCP clients.

It can help confirm that the laptop received an address from the DHCP server.

---

# Connectivity Testing

## 30. Ping DHCP Server

On the laptop:

```powershell
ping 192.168.10.1
```

### Explanation

Tests network connectivity to the specified IP address.

### Why I used it

I used ping to verify that the laptop could communicate with the network/DHCP server side.

> Replace `192.168.10.1` with the actual DHCP server IP if your server uses a different address.

---

# Final DHCP Testing Sequence

The complete testing process was:

### On Linux DHCP Server

```bash
ip addr
```

Check the network interface.

```bash
sudo systemctl status isc-dhcp-server
```

Check DHCP service.

```bash
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf
```

Check configuration syntax.

```bash
sudo systemctl restart isc-dhcp-server
```

Restart DHCP after configuration changes.

```bash
sudo journalctl -u isc-dhcp-server -n 50
```

Check DHCP logs.

### On Windows Laptop

```powershell
ipconfig /all
```

Check current network configuration and MAC address.

```powershell
ipconfig /release
```

Release the existing DHCP address.

```powershell
ipconfig /renew
```

Request a new address from the DHCP server.

```powershell
ipconfig
```

Verify the assigned IP address.

```powershell
ping <DHCP-server-IP>
```

Test connectivity.

---

# Overall Command Flow

```text
Check Network
     ↓
ip addr
     ↓
ip link
     ↓
ip route
     ↓
Update Packages
     ↓
sudo apt update
     ↓
Install DHCP
     ↓
sudo apt install isc-dhcp-server
     ↓
Configure DHCP
     ↓
sudo nano /etc/dhcp/dhcpd.conf
     ↓
Test Configuration
     ↓
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf
     ↓
Start / Restart DHCP
     ↓
sudo systemctl restart isc-dhcp-server
     ↓
Check Status
     ↓
sudo systemctl status isc-dhcp-server
     ↓
Connect Laptop through Switch
     ↓
ipconfig /all
     ↓
ipconfig /release
     ↓
ipconfig /renew
     ↓
ipconfig
     ↓
Verify Automatic IP Assignment
     ↓
Find Laptop MAC Address
     ↓
getmac
     ↓
Configure DHCP Reservation
     ↓
Restart DHCP
     ↓
Release + Renew
     ↓
Verify Reserved IP
     ↓
DHCP TASK COMPLETED
```

# Commands Actually Relevant to My Task

| Command                                    | Purpose                                    |
| ------------------------------------------ | ------------------------------------------ |
| `ip addr`                                  | Check Linux IP addresses and interfaces    |
| `ip link`                                  | Check network interface status             |
| `ip route`                                 | Check routing table                        |
| `sudo apt update`                          | Update package information                 |
| `sudo apt install isc-dhcp-server`         | Install DHCP server                        |
| `dpkg -l \| grep isc-dhcp-server`          | Verify DHCP installation                   |
| `sudo systemctl status isc-dhcp-server`    | Check DHCP service                         |
| `sudo systemctl start isc-dhcp-server`     | Start DHCP service                         |
| `sudo systemctl restart isc-dhcp-server`   | Reload DHCP configuration                  |
| `sudo systemctl enable isc-dhcp-server`    | Start DHCP automatically at boot           |
| `sudo nano /etc/dhcp/dhcpd.conf`           | Edit DHCP configuration                    |
| `sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf`   | Test DHCP configuration                    |
| `ipconfig`                                 | Check Windows IP address                   |
| `ipconfig /all`                            | Check detailed Windows network information |
| `ipconfig /release`                        | Release DHCP address                       |
| `ipconfig /renew`                          | Request DHCP address                       |
| `getmac`                                   | Find laptop MAC address                    |
| `sudo journalctl -u isc-dhcp-server`       | Check DHCP logs                            |
| `sudo journalctl -u isc-dhcp-server -n 50` | Check recent DHCP logs                     |
| `sudo cat /var/lib/dhcp/dhcpd.leases`      | Check DHCP leases                          |
| `ping <IP>`                                | Test network connectivity                  |

## Conclusion

The commands above were used during my **DHCP Server Installation, Configuration, Reservation, and Testing task**. The process started with checking the Linux network interface, installing the ISC DHCP server, configuring the DHCP network range, testing the configuration, and verifying the DHCP service. The DHCP server and laptop were then connected through a network switch, and the laptop successfully obtained an IP address automatically.

After confirming normal DHCP operation, I identified the laptop's MAC address and configured a DHCP reservation. The DHCP service was restarted, the laptop's DHCP lease was renewed, and the reserved IP address was verified. Therefore, the complete DHCP installation, configuration, automatic IP assignment, reservation, and testing process was successfully completed.
