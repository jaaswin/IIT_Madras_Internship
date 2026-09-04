

# Day 3 – Continued Network Troubleshooting and Technical Learning

On the third day of my internship, I continued observing the **Network Team's troubleshooting activities related to high CPU utilization in network switches**, which was a continuation of the investigation carried out on **Day 2**. Along with the troubleshooting activity, I studied several important networking and system administration concepts to understand the practical environment better.

## 1. Continued CPU Utilization Troubleshooting

The investigation into **high CPU utilization in network switches** continued from Day 2. The Network Team carried out a test case to investigate whether **IPv6 processing** could be contributing to the high CPU utilization.

### Troubleshooting Activity

* The team selected specific network switches for a **controlled test**.
* IPv6 was temporarily **disabled on the selected switches** to observe whether CPU utilization would decrease.
* The devices were monitored after the configuration change to observe both **CPU utilization and network performance**.
* Following the change, several **complaints and connectivity issues** were reported, particularly affecting certain network protocols and applications.
* This indicated that some services and applications were dependent on or affected by **IPv6 connectivity**.
* Although the test was intended to investigate CPU utilization, the resulting service impact made the configuration unsuitable for normal operation.
* The team therefore **re-enabled IPv6** and restored the switches to their previous configuration.
* The test was considered **unsuccessful as a solution**, because any potential CPU benefit did not justify the disruption to network services.
* The investigation into the root cause of the **high CPU utilization** was continued.

### Troubleshooting Approach Learned

I understood that practical network troubleshooting generally follows a systematic process:

**Identify the Problem → Analyze Possible Causes → Form a Hypothesis → Test on Selected Devices → Monitor Results → Check Service Impact → Evaluate the Solution → Roll Back if Required**

This helped me understand that a solution must be evaluated not only based on whether it improves CPU utilization, but also on its **impact on users, applications, protocols, and overall network availability**.

---

# 2. Study of the OSI Model

I studied the **OSI (Open Systems Interconnection) model** and its seven layers to understand how data communication takes place across a network.

| Layer | Name         | Main Function                                  |
| ----- | ------------ | ---------------------------------------------- |
| 7     | Application  | Provides network services to applications      |
| 6     | Presentation | Data formatting, encryption and compression    |
| 5     | Session      | Establishes and manages communication sessions |
| 4     | Transport    | End-to-end communication using TCP/UDP         |
| 3     | Network      | IP addressing and routing                      |
| 2     | Data Link    | MAC addressing and frame delivery              |
| 1     | Physical     | Transmission of bits through physical media    |

### Practical Understanding

For example, when a computer accesses a website, data passes through several networking components:

**Computer → Switch → Router → Firewall → ISP → Internet → Web Server**

I learned how the different OSI layers contribute to this communication and how devices such as **switches and routers** operate primarily at different layers.

---

# 3. Networking Devices

I studied the basic operation and purpose of common networking devices:

### Hub

A hub broadcasts incoming data to **all connected devices**. It primarily operates at the **Physical Layer**.

### Switch

A switch connects devices within a LAN and forwards frames based on **MAC addresses**. It primarily operates at the **Data Link Layer**.

### Router

A router connects different networks and forwards packets based on **IP addresses**. It primarily operates at the **Network Layer**.

### Firewall

A firewall monitors and controls network traffic according to predefined **security rules and policies**. It helps protect networks from unauthorized or unwanted traffic.

---

# 4. Optical Fiber and Data Transmission

I studied how data is transmitted through **optical fiber** and how it forms an important part of modern communication networks.

The basic communication process is:

**Digital Data → Electrical Signal → Optical Transmitter → Light Pulses → Optical Fiber → Optical Receiver → Electrical Signal → Digital Data**

The information is transmitted through the fiber as **light pulses**.

I also learned about two major types of optical fiber:

* **Single-Mode Fiber (SMF):** Used mainly for long-distance and high-bandwidth communication.
* **Multi-Mode Fiber (MMF):** Generally used for shorter-distance communication, such as within buildings and data centers.

I gained a basic understanding of how optical fiber can carry large amounts of data over long distances with low signal loss.

---

# 5. Understanding the Internet and Network Communication

I studied the basic path followed by data when a user accesses an online service.

A simplified path is:

**User Device → Access Switch → Router → Firewall → ISP → Internet → Destination Server**

I learned that the Internet is a **network of interconnected networks**, where routers forward packets between different networks using IP addressing and routing protocols.

This helped me connect the theoretical concepts of the OSI model with the practical network infrastructure observed during the internship.

---

# 6. Operating System and Kernel

I also studied the fundamentals of an **Operating System (OS)**.

An operating system acts as an interface between **hardware and software** and manages system resources.

Major functions include:

* Process management
* Memory management
* File management
* Device management
* User management
* Security
* Networking

### Kernel

I learned that the **kernel is the core component of an operating system**. It provides communication between applications and hardware and manages important resources such as:

**Applications → System Calls → Kernel → Hardware**

The kernel manages CPU, memory, storage, and hardware devices while providing the necessary services for applications.

---

# 7. BIOS, UEFI, MBR and GPT

I studied the basic concepts involved in the computer boot process and disk partitioning.

### BIOS

**BIOS (Basic Input/Output System)** is traditional firmware that initializes hardware and starts the operating system boot process.

### UEFI

**UEFI (Unified Extensible Firmware Interface)** is the modern replacement for BIOS. It provides improved boot functionality and works well with modern hardware and GPT partitioning.

### MBR

**MBR (Master Boot Record)** is an older disk partitioning scheme with limitations on disk size and partition structure.

### GPT

**GPT (GUID Partition Table)** is a modern partitioning scheme that supports larger storage devices and a larger number of partitions. It is commonly used with **UEFI** systems.

### Basic Relationship

**Older Systems:**
BIOS → MBR → Operating System

**Modern Systems:**
UEFI → GPT → Operating System

---

## Key Learning of Day 3

Day 3 provided both **practical network troubleshooting exposure and theoretical learning**. I observed the continuation of the high CPU utilization investigation from Day 2 and understood how a real network team tests a possible cause, monitors the impact, and rolls back a change when it affects network services.

Along with this practical exposure, I strengthened my understanding of the **OSI model, switches, routers, hubs, firewalls, optical fiber, Internet communication, operating systems, kernels, BIOS, UEFI, MBR, and GPT**.

The major takeaway was that **network troubleshooting is not simply about fixing one technical parameter. A successful solution must improve the problem without negatively affecting the overall network and its users.**
