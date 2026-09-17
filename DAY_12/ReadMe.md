# Day 12 – DNS Documentation, DoS/DDoS Study and New Task Assignment

## 1. Overview

On the twelfth day of my internship, I focused on documenting the DNS installation, configuration, and testing task completed earlier. I organized the configuration steps, commands, testing results, and observations for adding them to the internship project repository.

I also studied **Denial of Service (DoS)** and **Distributed Denial of Service (DDoS)** attacks in detail, including their working, types, effects, detection, and mitigation techniques. At the end of the day, a new practical task was assigned to create a controlled three-machine environment for demonstrating secure file-upload communication, DDoS detection, and mitigation.

---

## 2. DNS Installation and Configuration Documentation

The DNS task involved setting up and testing a DNS server in an Ubuntu environment.

### Activities Documented

* DNS server installation
* DNS configuration
* DNS record configuration
* DNS service management
* DNS testing
* Name resolution verification
* Recording commands and screenshots
* Organizing the completed work in the GitHub repository

The DNS configuration was tested by performing domain-name resolution and connectivity checks. Successful responses confirmed that DNS resolution was functioning correctly.

### Learning Outcome

I understood how DNS converts human-readable domain names into IP addresses and how a DNS server supports communication between clients and network services.

---

# 3. Study of DoS and DDoS

## 3.1 What is DoS?

**Denial of Service (DoS)** is an attack in which a service, server, or network resource is overwhelmed with excessive requests or traffic, making it difficult or impossible for legitimate users to access the service.

The attacker attempts to consume resources such as:

* Network bandwidth
* CPU
* Memory
* Connection resources
* Application resources

### Basic Flow

```text
Attacker
    |
    | Excessive traffic/requests
    v
Target Server
    |
    X
Service becomes unavailable
```

---

## 3.2 What is DDoS?

**Distributed Denial of Service (DDoS)** is a DoS attack where excessive traffic or requests originate from multiple systems.

These systems may form a **botnet**, which can be controlled by an attacker to send traffic toward a target.

```text
Machine A ──┐
Machine B ──┤
Machine C ──┼──► Target Server
Machine D ──┤
Machine E ──┘
```

The distributed nature of the traffic makes detection and mitigation more challenging.

---

## 3.3 Difference Between DoS and DDoS

| Feature         | DoS                           | DDoS                                            |
| --------------- | ----------------------------- | ----------------------------------------------- |
| Full form       | Denial of Service             | Distributed Denial of Service                   |
| Traffic sources | Usually one source            | Multiple sources                                |
| Distribution    | Centralized                   | Distributed                                     |
| Detection       | Comparatively simpler         | More challenging                                |
| Mitigation      | Can often focus on the source | Requires broader traffic analysis and filtering |

---

## 3.4 Types of DoS/DDoS Attacks

### Volumetric Attacks

These attempt to consume the available network bandwidth by generating a large volume of traffic.

### Protocol Attacks

These target network or protocol processing resources and can consume resources on network devices or servers.

### Application-Layer Attacks

These target application services by sending a large number of requests that appear similar to legitimate application traffic.

---

# 4. DoS/DDoS Detection

Network teams can monitor several indicators to identify abnormal traffic:

* Sudden increase in request rate
* Unusual network bandwidth consumption
* High CPU utilization
* Large number of connections
* Repeated requests from a source
* Unusual traffic patterns
* Increase in failed requests
* Unexpected changes in server response time

A basic detection concept is:

```text
Incoming Traffic
       |
       v
Traffic Monitoring
       |
       v
Analyze Request Pattern
       |
       v
Is Traffic Abnormal?
     /       \
   No         Yes
   |           |
Normal      Generate Alert
Traffic
```

---

# 5. DoS/DDoS Mitigation

Common defensive techniques include:

* Rate limiting
* Traffic filtering
* Firewall rules
* Source blocking
* Load balancing
* CDN-based protection
* Monitoring and alerting
* Distributed infrastructure

### Rate Limiting

Rate limiting restricts how many requests a client can send within a specified period.

```text
Client
  |
  | Requests
  v
Rate Limiter
  |
  ├── Normal rate → Allow
  |
  └── Excessive rate → Limit/Block
```

The purpose is to reduce abnormal traffic while keeping legitimate communication available.

---

# 6. New Task Assigned

A new practical task was assigned to create a **controlled three-machine network environment** for demonstrating secure file-upload communication and DDoS detection and mitigation.

### Machine Roles

| Machine   | Role                                                      |
| --------- | --------------------------------------------------------- |
| Machine 1 | Legitimate client                                         |
| Machine 2 | Controlled DDoS traffic generator                         |
| Machine 3 | File-upload server, traffic monitor and mitigation system |

### Task Flow

```text
Machine 1
Legitimate File Upload
       |
       v
Machine 3
File Upload Server
       ^
       |
Excessive Requests
       |
Machine 2
Controlled Traffic Generator

Machine 3:
Monitor → Detect → Alert → Mitigate → Verify
```

---

## 7. Planned Task Activities

The practical task will be performed in a controlled and isolated lab environment.

### Phase 1 – Network Setup

Configure the three machines on the same isolated network and verify communication between them.

### Phase 2 – File Upload Service

Configure Machine 3 as a file-upload server and verify that Machine 1 can upload files successfully.

### Phase 3 – Controlled Traffic Generation

Use Machine 2 to generate controlled excessive requests toward Machine 3 for testing the detection mechanism.

### Phase 4 – Traffic Monitoring

Monitor incoming requests, traffic rate, source information, server resources, and response behavior.

### Phase 5 – Detection and Alert

Identify abnormal request patterns and generate an alert when the defined threshold is exceeded.

### Phase 6 – Mitigation

Apply a defensive mechanism such as rate limiting or controlled source blocking.

### Phase 7 – Verification

Verify that:

* Abnormal traffic is reduced or controlled.
* The server remains available.
* Machine 1 can still perform legitimate file uploads.

---

# 8. Learning Outcome

By the end of Day 12, I:

* Documented the previously completed DNS installation and configuration task.
* Improved my understanding of DNS operation and testing.
* Studied DoS and DDoS attacks in detail.
* Learned about different categories of DoS/DDoS attacks.
* Studied methods used to detect abnormal network traffic.
* Learned about common DDoS mitigation techniques.
* Understood the importance of protecting legitimate traffic during mitigation.
* Received a new practical task involving controlled DDoS detection and mitigation.

## Conclusion

Day 12 focused on consolidating the previous DNS work through proper documentation and expanding my networking knowledge through the study of DoS and DDoS attacks. A new practical task was also assigned to build a controlled three-machine environment that demonstrates traffic monitoring, abnormal traffic detection, alert generation, mitigation, and verification of legitimate file-upload communication.
