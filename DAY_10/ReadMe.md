# Day 10 – Networking Concepts and Internet Infrastructure

## Objective

The objective of Day 10 was to strengthen my understanding of important networking concepts used in real-world network infrastructure. I studied **IP addressing, MAC addressing, subnetting, DNS, CDN, and the relationship between different layers of network communication**.

## Topics Studied

### 1. IP Addressing

I studied the purpose of IP addresses and how they are used to identify devices and enable communication across networks.

* **IPv4:** Uses a 32-bit address, such as `192.168.1.10`.
* **IPv6:** Uses a 128-bit address and provides a much larger address space.
* Learned the difference between **private and public IP addresses**.
* Studied the role of the **subnet mask** in dividing networks into smaller sections.
* Understood how the **default gateway** allows devices to communicate outside their local network.

### 2. MAC Addressing

I learned about MAC addresses and their role in local network communication.

* A MAC address is associated with a network interface.
* It operates mainly at the **Data Link Layer (Layer 2)**.
* Switches use MAC addresses to forward Ethernet frames.
* Studied the difference between **MAC address and IP address**.
* Connected this concept with DHCP reservations, where a device's MAC address can be mapped to a fixed IP address.

### 3. CDN – Content Delivery Network

I studied the basic concept and working of a CDN.

A **Content Delivery Network (CDN)** is a distributed network of servers used to deliver web content closer to users.

Basic working:

**User → DNS → CDN/Edge Server → Content**

I learned that CDNs can reduce latency by serving content from an appropriate **edge location** instead of always contacting the origin server.

I also studied the role of:

* Origin server
* Edge server
* Point of Presence (PoP)
* Caching
* DNS in directing users toward CDN services
* CDN use for websites, images, videos, JavaScript, and other static content

### 4. DNS and Network Communication

I revised DNS and understood its relationship with IP addressing and CDN.

When a user enters a domain name, DNS helps resolve the domain into an IP address. In CDN environments, DNS can also participate in directing users toward suitable CDN infrastructure.

Example:

**User → DNS Resolution → CDN Edge → Website Content**

### 5. ARP and Local Network Communication

I also studied the basic purpose of **ARP (Address Resolution Protocol)**.

ARP is used in IPv4 networks to determine the MAC address associated with a known IP address on the local network.

Example:

**IP Address → ARP → MAC Address → Ethernet Frame**

This helped me understand how IP addressing and MAC addressing work together during local network communication.

## Key Understanding

The main understanding from Day 10 was that different networking concepts work together rather than operating independently.

**DNS** helps resolve names, **IP addresses** identify devices or network endpoints, **MAC addresses** are used for local Layer 2 communication, and **CDNs** improve content delivery by placing cached content closer to users.

## Conclusion

On Day 10, I strengthened my fundamental networking knowledge by studying IP addressing, MAC addressing, CDN architecture, DNS, ARP, subnetting, and network communication. These concepts helped me better understand how devices communicate within a local network and how users access services across the Internet.
