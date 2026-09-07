# Day 05 – Completion of DHCP Server Configuration, Testing and DHCP Reservation

## 1. Continuation of Previous Day's Task

On Day 04, I started the practical task of installing and configuring a **DHCP server on Linux**. The DHCP server package was successfully installed, but I was unable to complete the configuration and client-side testing because I needed a better understanding of Linux commands, IP addressing, subnetting, MAC addressing, and DHCP configuration parameters.

On Day 05, I continued the pending task by first reviewing the required networking concepts and then completing the **DHCP server configuration, network testing, and DHCP reservation**.

The complete task was successfully completed by the end of the session.

---

# 2. Task Objective

The objective was to set up a working DHCP server and verify its operation with a client laptop.

The task included:

* Complete the DHCP server configuration.
* Configure the DHCP network and IP address range.
* Connect the DHCP server and laptop through a network switch.
* Configure the laptop to obtain an IP address automatically.
* Verify that the DHCP server assigns an IP address to the laptop.
* Identify the laptop's MAC address.
* Configure a DHCP reservation.
* Assign a fixed IP address to the laptop through DHCP.
* Renew the DHCP lease and verify the reserved IP address.
* Confirm that the complete DHCP setup is working correctly.

### Network Setup

**Linux DHCP Server → Network Switch → Laptop**

---

# 3. Review of Basic Networking Concepts

Before continuing the configuration, I reviewed the basic concepts required to understand the DHCP setup.

### 3.1 IP Address

An IP address identifies a device on an IP network and allows devices to communicate with each other.

For the DHCP setup, I needed to understand the difference between the:

* Network address
* Server IP address
* Client IP address
* DHCP address range
* Default gateway

### 3.2 MAC Address

A MAC address is the hardware address associated with a network interface.

The MAC address of the laptop was required later for configuring the DHCP reservation.

### 3.3 Subnet Mask

The subnet mask determines which portion of an IP address represents the network and which portion represents the host.

Understanding the subnet mask was necessary for defining the DHCP network correctly.

### 3.4 DHCP

DHCP automatically provides network configuration information to client devices.

The basic DHCP process can be understood as:

**Client → DHCP Discover → DHCP Offer → DHCP Request → DHCP Acknowledgement**

This process allows a client to obtain an IP address and other network configuration automatically.

---

# 4. Completing the DHCP Server Configuration

After reviewing the networking fundamentals, I continued with the DHCP configuration on the Linux system.

The DHCP configuration was prepared according to the network used for the practical test.

The configuration included:

* DHCP network address
* Subnet mask
* IP address range
* Default gateway
* DNS server
* Lease duration

The IP address range defines the group of addresses that the DHCP server can provide to client devices.

For example, if the configured DHCP pool contains a range of addresses, the server selects an available address from that pool and assigns it to the requesting client.

### Configuration Status

**DHCP Server Configuration: ✅ Completed**

---

# 5. Applying and Verifying the Configuration

After completing the configuration, I applied the changes and checked whether the DHCP service was running correctly.

The service status was verified to ensure that the DHCP server was active and ready to respond to client requests.

This step was important because a configuration file can contain errors that prevent the DHCP service from starting.

After correcting and verifying the configuration, the DHCP service was successfully prepared for testing.

**Status: ✅ Completed**

---

# 6. Connecting the DHCP Server and Laptop

The next step was to perform the practical test using a network switch.

The Linux system running the DHCP server and the laptop were connected to the same network switch.

### Physical Network Setup

**Linux DHCP Server**
↓
**Network Switch**
↓
**Laptop**

The laptop was configured to obtain its IP address automatically instead of using a manually assigned static IP address.

---

# 7. Testing Automatic IP Address Assignment

After connecting the laptop to the switch, I checked whether the laptop could communicate with the DHCP server.

The laptop sent a DHCP request to obtain network configuration.

The DHCP server responded by assigning an available IP address from the configured DHCP range.

The laptop successfully received its network configuration.

The assigned information included:

* IP address
* Subnet mask
* Default gateway
* DNS server information

This confirmed that the DHCP server was successfully communicating with the client laptop.

### Test Result

**Automatic DHCP Assignment: ✅ Successfully Completed**

---

# 8. Verifying the Client IP Configuration

After the laptop received an IP address, I verified the network configuration on the laptop.

The purpose of this verification was to confirm that:

1. The laptop received an IP address from the DHCP server.
2. The assigned IP address belonged to the configured DHCP range.
3. The subnet mask was correct.
4. The default gateway information was correctly provided.
5. DNS information was received as configured.

This helped confirm that the DHCP server was not only running, but also providing the required network configuration to the client.

**Status: ✅ Verified**

---

# 9. Identifying the Laptop MAC Address

After successfully testing normal DHCP allocation, I moved to the next part of the task, which was configuring a **DHCP reservation**.

For a reservation, the DHCP server needs to identify a particular client.

The laptop's **MAC address** was identified from its network configuration.

The MAC address acts as the identifier for the laptop's network interface.

The reservation could then associate:

**Laptop MAC Address → Specific IP Address**

---

# 10. DHCP Reservation Configuration

A DHCP reservation was configured for the laptop.

A reservation tells the DHCP server to provide a particular IP address to a specific device based on its MAC address.

For example:

**MAC Address of Laptop → Reserved IP Address**

This is different from normal dynamic DHCP allocation.

### Normal DHCP

The server selects an available IP address from the DHCP pool.

### DHCP Reservation

The server identifies the client using its MAC address and provides the specific IP address configured for that client.

This is useful when a device needs to consistently receive the same IP address while still using DHCP.

---

# 11. Applying the DHCP Reservation

After adding the laptop's MAC address and the reserved IP address to the DHCP configuration, the updated configuration was applied.

The DHCP service was then checked to ensure that the updated configuration was accepted without errors.

The reservation was successfully added to the DHCP server.

**DHCP Reservation Status: ✅ Completed**

---

# 12. Testing the DHCP Reservation

After configuring the reservation, the laptop's DHCP lease was renewed.

The purpose of this test was to verify whether the DHCP server would provide the reserved IP address to the laptop.

The laptop requested network configuration again, and the DHCP server identified the client using its MAC address.

The server then assigned the IP address configured for that MAC address.

The laptop successfully received the **reserved IP address**.

### Reservation Test Result

**Reserved IP Assignment: ✅ Successfully Completed**

---

# 13. Final DHCP Verification

After completing both dynamic DHCP assignment and reservation testing, the complete setup was verified.

The following sequence was successfully tested:

**DHCP Server Installation**
↓
**DHCP Configuration**
↓
**Server Started and Verified**
↓
**Server Connected to Switch**
↓
**Laptop Connected to Switch**
↓
**Laptop Requested IP Address**
↓
**DHCP Server Assigned IP Address**
↓
**Laptop MAC Address Identified**
↓
**DHCP Reservation Configured**
↓
**DHCP Lease Renewed**
↓
**Reserved IP Address Received**
↓
**Final Verification Completed**

---

# 14. Task Status

> ## 🟢 OVERALL TASK: SUCCESSFULLY COMPLETED
>
> **DHCP Server Installation:** ✅ Completed
>
> **DHCP Network Configuration:** ✅ Completed
>
> **DHCP Service Verification:** ✅ Completed
>
> **Network Switch Connection:** ✅ Completed
>
> **Laptop Connection:** ✅ Completed
>
> **Automatic IP Address Assignment:** ✅ Successfully Tested
>
> **IP Configuration Verification:** ✅ Completed
>
> **Laptop MAC Address Identification:** ✅ Completed
>
> **DHCP Reservation Configuration:** ✅ Completed
>
> **Reserved IP Address Testing:** ✅ Successfully Tested
>
> **Final DHCP Verification:** ✅ Completed

---

# 15. Problems Faced and Resolution

The main challenge was initially understanding the Linux commands and DHCP configuration parameters.

On Day 04, this knowledge gap prevented me from completing the configuration.

On Day 05, I focused on understanding the purpose of the networking parameters and the relationship between:

**IP Address + Subnet Mask + Network Interface + DHCP Range + MAC Address**

Once these concepts were understood, I was able to continue the configuration and complete the testing successfully.

This experience also showed me that troubleshooting a network service requires understanding both the **Linux system** and the **networking concepts** involved.

---

# 16. Learning Outcomes

By completing this task, I gained practical knowledge of DHCP server administration and basic Linux networking.

The main concepts I learned were:

* How to install a DHCP server on Linux.
* How to configure a DHCP network.
* How to define a DHCP IP address pool.
* How DHCP assigns IP addresses to client devices.
* How a laptop obtains network configuration automatically.
* How to identify a device using its MAC address.
* How DHCP reservations work.
* How to associate a MAC address with a specific IP address.
* How to renew a DHCP lease.
* How to verify DHCP-assigned network information.
* How to test DHCP using a physical network switch.
* How to troubleshoot DHCP configuration problems.
* The importance of understanding Linux commands while managing network services.

---

# 17. Overall Learning

The completion of this task gave me my first practical experience in setting up a network service and testing it with a real client device.

Initially, I had difficulty understanding the configuration because of limited knowledge of Linux commands and networking fundamentals. By continuing the task and understanding the purpose of each configuration parameter, I was able to complete the DHCP setup.

The task also helped me understand the practical relationship between **IP addressing, MAC addressing, DHCP, network switches, Linux configuration, and client devices**.

---

# 18. Conclusion

The DHCP server task that was started on Day 04 was successfully completed on Day 05.

I completed the **DHCP server installation and configuration**, connected the server and laptop through a network switch, and successfully tested automatic IP address assignment.

After confirming normal DHCP operation, I configured a **DHCP reservation using the laptop's MAC address** and successfully verified that the laptop received the reserved IP address after renewing its DHCP lease.

Overall, this task provided valuable hands-on experience with **Linux DHCP server administration, IP addressing, MAC addressing, DHCP address allocation, DHCP reservations, network switches, and basic network troubleshooting**.
