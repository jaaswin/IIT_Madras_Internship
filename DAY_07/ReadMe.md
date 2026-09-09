# DNS Server Installation, Configuration and Testing

## 1. Introduction

As part of my internship training, I performed the installation, configuration, and testing of a **DNS (Domain Name System) server** on Linux.

DNS is an important networking service that translates human-readable domain names such as:

> `www.example.com`

into IP addresses that computers use to communicate over a network.

The task included installing the DNS server software, configuring the DNS service, starting and verifying the service, testing DNS name resolution, and performing a client-side connectivity test.

---

# 2. Objective

The main objectives of this task were:

* Understand the purpose of DNS.
* Install a DNS server on Linux.
* Configure the DNS service.
* Verify that the DNS service is running.
* Test DNS name resolution.
* Test DNS resolution from a client system.
* Verify connectivity using `ping`.
* Troubleshoot basic DNS-related issues.

---

# 3. Basic Understanding of DNS

DNS stands for **Domain Name System**.

When a user enters a domain name such as:

> `www.example.com`

the computer needs the corresponding IP address to communicate with the destination server.

The basic process is:

```text
User enters www.example.com
          ↓
DNS Resolver
          ↓
DNS Server
          ↓
IP Address is obtained
          ↓
Computer connects to the destination
```

For example:

```text
www.example.com
       ↓
DNS Resolution
       ↓
IP Address
```

This allows users to access websites using domain names instead of remembering numerical IP addresses.

---

# 4. Check Linux Network Configuration

Before configuring DNS, I checked the network configuration of the Linux system.

### `ip addr`

**Explanation:**
Displays the network interfaces and their assigned IP addresses.

**Purpose:**
Used to identify the active network interface and verify network connectivity.

---

### `ip route`

**Explanation:**
Displays the routing table of the Linux system.

**Purpose:**
Used to check the default gateway and routing information.

---

# 5. Update Package Information

### `sudo apt update`

**Explanation:**
Updates the local package information from the Ubuntu software repositories.

**Purpose:**
Used before installing the DNS server package to ensure the available package information is up to date.

---

# 6. Install DNS Server

For this task, the DNS server software used was **BIND9**.

### `sudo apt install bind9`

**Explanation:**
Installs the BIND9 DNS server package on Ubuntu/Linux.

**Purpose:**
Used to install the DNS server software required for the task.

BIND9 provides the required services for handling DNS queries and name resolution.

---

# 7. Install DNS Utilities

### `sudo apt install dnsutils`

**Explanation:**
Installs useful DNS testing utilities such as `nslookup` and `dig`.

**Purpose:**
Used to test DNS resolution and verify whether the DNS server is responding correctly.

---

# 8. Check DNS Service Status

### `sudo systemctl status bind9`

**Explanation:**
Displays the current status of the BIND9 DNS service.

**Purpose:**
Used to verify whether the DNS server is running correctly.

A successful service should show a status similar to:

```text
Active: active (running)
```

---

# 9. Start DNS Service

### `sudo systemctl start bind9`

**Explanation:**
Starts the BIND9 DNS server service.

**Purpose:**
Used if the DNS service is not already running.

---

# 10. Restart DNS Service

### `sudo systemctl restart bind9`

**Explanation:**
Restarts the BIND9 DNS service.

**Purpose:**
Used after making configuration changes so that the DNS server loads the updated configuration.

---

# 11. Enable DNS Service at Boot

### `sudo systemctl enable bind9`

**Explanation:**
Configures BIND9 to start automatically when the Linux system boots.

**Purpose:**
Ensures that the DNS service is available after a system restart.

---

# 12. Check DNS Configuration Files

BIND9 uses configuration files stored mainly under:

```text
/etc/bind/
```

The important configuration files include:

```text
/etc/bind/named.conf
/etc/bind/named.conf.options
/etc/bind/named.conf.local
```

---

# 13. Open DNS Options Configuration

### `sudo nano /etc/bind/named.conf.options`

**Explanation:**
Opens the BIND9 options configuration file.

**Purpose:**
Used to configure DNS server options such as forwarding and query behavior.

---

# 14. Configure DNS Forwarder

A DNS forwarder can be configured to forward DNS queries to another DNS server when the local DNS server does not have the required information.

Example configuration:

```conf
options {
        directory "/var/cache/bind";

        forwarders {
                8.8.8.8;
                1.1.1.1;
        };

        dnssec-validation auto;

        listen-on-v6 { any; };
};
```

### Explanation

The forwarders are:

```text
8.8.8.8
1.1.1.1
```

These are external DNS resolvers.

The local BIND9 server can forward queries to them when required.

---

# 15. Check BIND9 Configuration

### `sudo named-checkconf`

**Explanation:**
Checks the BIND9 configuration files for syntax errors.

**Purpose:**
Used to verify that the DNS configuration was written correctly before restarting the service.

If there is no output, the configuration syntax is generally valid.

---

# 16. Check DNS Service Again

### `sudo systemctl status bind9`

**Explanation:**
Checks whether BIND9 is running after the configuration changes.

**Purpose:**
Used to confirm that the DNS service successfully started with the updated configuration.

---

# 17. Test DNS Resolution Using nslookup

### `nslookup www.example.com`

**Explanation:**
Performs a DNS lookup for `www.example.com`.

It displays information such as:

* DNS server used
* Domain name
* Resolved IP address

**Purpose:**
Used to verify that the DNS server can resolve a domain name into an IP address.

Example:

```text
Server:    ...
Address:   ...

Name:      www.example.com
Address:   ...
```

The exact IP address returned may vary.

---

# 18. Test DNS Resolution Using dig

### `dig www.example.com`

**Explanation:**
Performs a detailed DNS query.

It provides information about:

* DNS server
* Query status
* Answer section
* Returned IP address
* Query time

**Purpose:**
Used for detailed DNS troubleshooting and verification.

---

# 19. Check DNS Resolver Configuration

### `resolvectl status`

**Explanation:**
Displays the DNS resolver configuration of the Linux system.

**Purpose:**
Used to check which DNS servers are being used by the Linux system.

---

# 20. Check resolv.conf

### `cat /etc/resolv.conf`

**Explanation:**
Displays the DNS resolver configuration file.

**Purpose:**
Used to check the configured nameserver information.

Example:

```text
nameserver 8.8.8.8
```

The actual configuration can vary depending on the Linux networking setup.

---

# 21. Test Internet Connectivity

### `ping 8.8.8.8`

**Explanation:**
Tests connectivity to the specified IP address without depending on DNS name resolution.

**Purpose:**
Used to determine whether the basic network connection is working.

---

# 22. Test DNS and Network Connectivity

### `ping www.example.com`

**Explanation:**
First requires DNS resolution of `www.example.com`, then sends ICMP packets to the resolved IP address.

**Purpose:**
Used to verify both:

1. DNS name resolution
2. Network connectivity

---

# 23. DNS Client Testing

After completing the DNS server configuration, I tested DNS resolution from the client system.

The client was tested using:

### `nslookup www.example.com`

**Purpose:**
To verify that the client could resolve the domain name successfully.

The DNS server returned an IP address for the requested domain.

---

# 24. Final Ping Test

The final test was performed using:

### `ping www.example.com`

The system successfully resolved the domain name and received replies from the resolved IP address.

Example result:

```text
Pinging www.example.com [IP_ADDRESS] with 32 bytes of data:
Reply from IP_ADDRESS: bytes=32 time=...
Reply from IP_ADDRESS: bytes=32 time=...
Reply from IP_ADDRESS: bytes=32 time=...
```

This confirmed that DNS resolution was working and the client could communicate with the resolved destination.

---

# 25. DNS Troubleshooting Commands

The following commands can be used when troubleshooting DNS problems.

### `sudo journalctl -u bind9`

**Explanation:**
Displays logs related to the BIND9 service.

**Purpose:**
Used to identify DNS service errors and events.

---

### `sudo journalctl -u bind9 -n 50`

**Explanation:**
Displays the latest 50 BIND9 log entries.

**Purpose:**
Used to quickly check recent DNS activity.

---

### `sudo ss -luntp | grep :53`

**Explanation:**
Checks whether a service is listening on DNS port `53`.

**Purpose:**
Used to verify that BIND9 is listening for DNS requests.

DNS normally uses:

```text
UDP port 53
TCP port 53
```

---

# 26. Complete DNS Testing Sequence

The overall testing process was:

```text
Check Network
      ↓
ip addr
      ↓
Check Routing
      ↓
ip route
      ↓
Update Packages
      ↓
sudo apt update
      ↓
Install BIND9
      ↓
sudo apt install bind9
      ↓
Install DNS Utilities
      ↓
sudo apt install dnsutils
      ↓
Check BIND9 Status
      ↓
sudo systemctl status bind9
      ↓
Configure DNS
      ↓
sudo nano /etc/bind/named.conf.options
      ↓
Check Configuration
      ↓
sudo named-checkconf
      ↓
Restart BIND9
      ↓
sudo systemctl restart bind9
      ↓
Test DNS Resolution
      ↓
nslookup www.example.com
      ↓
Ping Test
      ↓
ping www.example.com
      ↓
DNS TASK COMPLETED
```

---

# 27. Commands Used in the DNS Task

| Command                                  | Purpose                                   |
| ---------------------------------------- | ----------------------------------------- |
| `ip addr`                                | Check network interfaces and IP addresses |
| `ip route`                               | Check routing information                 |
| `sudo apt update`                        | Update package information                |
| `sudo apt install bind9`                 | Install BIND9 DNS server                  |
| `sudo apt install dnsutils`              | Install DNS testing tools                 |
| `sudo systemctl status bind9`            | Check DNS service status                  |
| `sudo systemctl start bind9`             | Start DNS service                         |
| `sudo systemctl restart bind9`           | Restart DNS service                       |
| `sudo systemctl enable bind9`            | Enable DNS service at boot                |
| `sudo nano /etc/bind/named.conf.options` | Edit DNS options                          |
| `sudo named-checkconf`                   | Check DNS configuration syntax            |
| `nslookup www.example.com`               | Test DNS name resolution                  |
| `dig www.example.com`                    | Perform detailed DNS query                |
| `resolvectl status`                      | Check DNS resolver configuration          |
| `cat /etc/resolv.conf`                   | View resolver configuration               |
| `ping 8.8.8.8`                           | Test IP connectivity                      |
| `ping www.example.com`                   | Test DNS resolution and connectivity      |
| `sudo journalctl -u bind9`               | View DNS service logs                     |
| `sudo ss -luntp \| grep :53`             | Check DNS port 53                         |

---

# 28. Result

The DNS server installation, configuration, and testing process was successfully completed.

The following activities were completed:

* BIND9 DNS server installed successfully.
* DNS service status verified.
* DNS configuration completed.
* DNS configuration syntax checked.
* BIND9 service restarted successfully.
* DNS utilities installed.
* Domain name resolution tested using `nslookup`.
* DNS query tested using `dig`.
* DNS resolution tested using `ping`.
* Client-side DNS resolution verified.
* Network connectivity verified.

The final test using:

> **`ping www.example.com`**

successfully resolved the domain name to an IP address and received replies.

---

# 29. Learning Outcomes

Through this task, I gained practical knowledge of:

* DNS and domain name resolution.
* BIND9 DNS server installation.
* Linux package management.
* Linux service management using `systemctl`.
* DNS configuration files.
* DNS forwarders.
* DNS troubleshooting.
* `nslookup` and `dig`.
* DNS port 53.
* Linux network configuration.
* Client-side DNS testing.
* Basic network troubleshooting.

---

# 30. Conclusion

The **DNS Server Installation, Configuration and Testing** task was successfully completed.

I installed the BIND9 DNS server on Linux and configured the required DNS options. The configuration was checked for errors and the DNS service was started and verified. DNS resolution was then tested using `nslookup` and `dig`.

Finally, the client system was tested using:

> **`ping www.example.com`**

The domain name was successfully resolved to an IP address and the system received replies. This confirmed that the DNS resolution and network connectivity were working correctly.

This task provided practical experience in **DNS administration, Linux server configuration, service management, DNS troubleshooting, and client-side network testing**.

**Status: COMPLETED ✅**
