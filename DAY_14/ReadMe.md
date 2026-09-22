# DAY 14 – DDoS Study, Documentation and Task Preparation

**Organization:** IIT Madras – Computer Centre
**Intern:** Jayaaswin M.

## 1. Introduction

On Day 14 of the internship, I focused on preparing the documentation for the assigned DDoS detection and mitigation task. I also studied the concepts of Denial-of-Service (DoS) and Distributed Denial-of-Service (DDoS) attacks in depth to understand their working, characteristics, detection methods, and mitigation techniques.

The assigned task involves creating a controlled three-machine network environment to demonstrate normal file-upload communication, abnormal traffic generation, DDoS detection, and mitigation.

## 2. Objectives

The main objectives of the day's activities were:

* To understand DoS and DDoS attacks in detail.
* To study the difference between DoS and DDoS.
* To understand different categories of DDoS attacks.
* To learn how abnormal network traffic can be detected.
* To study common DDoS mitigation techniques.
* To understand the architecture of the assigned three-machine environment.
* To prepare the documentation and requirements for the practical implementation.

## 3. DoS and DDoS

### Denial-of-Service (DoS)

A Denial-of-Service attack attempts to make a service, server, or network resource unavailable to legitimate users by overwhelming or exhausting its available resources.

A DoS attack may originate from a single system or a limited number of sources.

### Distributed Denial-of-Service (DDoS)

A Distributed Denial-of-Service attack uses multiple systems or sources to generate traffic or requests toward a target. The distributed nature makes identifying and filtering the unwanted traffic more challenging.

The general concept can be represented as:

**Multiple Sources → Network → Target Server → Service Degradation**

## 4. Difference Between DoS and DDoS

| Feature        | DoS                                | DDoS                                                 |
| -------------- | ---------------------------------- | ---------------------------------------------------- |
| Sources        | Usually a single or limited source | Multiple distributed sources                         |
| Traffic origin | Relatively easier to identify      | More difficult to identify                           |
| Scale          | Generally smaller                  | Can be distributed across many systems               |
| Detection      | Comparatively simpler              | Requires more detailed traffic analysis              |
| Mitigation     | Source filtering can be simpler    | Requires filtering, rate limiting and other controls |

## 5. Categories of DDoS Attacks

During the study, I learned about three broad categories of DDoS attacks.

### 5.1 Volumetric Attacks

These attacks attempt to consume available network bandwidth by generating a large volume of traffic toward the target.

The main objective is to create network congestion and reduce the availability of the service.

### 5.2 Protocol Attacks

Protocol attacks target weaknesses or resource limitations in network and transport-layer protocols or network devices.

They can result in increased processing requirements and exhaustion of resources such as connection tables.

### 5.3 Application-Layer Attacks

Application-layer attacks target services or applications directly by generating a large number of requests.

These attacks may consume server resources such as CPU, memory, database connections, or application threads even when the total network bandwidth is not extremely high.

## 6. DDoS Detection Indicators

I studied several indicators that can help identify abnormal traffic conditions:

* Sudden increase in incoming traffic.
* Large number of requests within a short period.
* Unusual number of connections.
* Increased CPU and memory utilization.
* Increased network bandwidth usage.
* Packet drops or retransmissions.
* Increased response time.
* Service slowdown or unavailability.
* Large difference between normal and abnormal traffic patterns.

Monitoring these parameters helps distinguish normal network activity from unusual traffic behavior.

## 7. DDoS Mitigation Techniques

The following defensive techniques were studied:

### Rate Limiting

Limits the number of requests or connections accepted from a source within a specific time period.

### Traffic Filtering

Filters unwanted or abnormal traffic using firewall rules and other network controls.

### IP-Based Blocking

Traffic from identified malicious or unwanted sources can be blocked when appropriate.

### Connection Limits

Limits the number of simultaneous connections that a service accepts.

### Monitoring and Alerting

Network and server monitoring tools can be used to identify sudden changes in traffic, CPU utilization, bandwidth, and connection activity.

### Distributed Protection

For larger environments, traffic can be distributed across multiple systems or protected using specialized network security infrastructure.

## 8. Assigned Three-Machine Environment

The assigned task uses three machines with different roles.

### Machine 1 – Legitimate Client

Machine 1 represents a normal user.

Its purpose is to:

* Connect to the server.
* Upload files.
* Generate legitimate application traffic.
* Verify that the server continues to provide normal service.

### Machine 2 – Controlled Traffic Generator

Machine 2 is used to generate controlled abnormal traffic within the authorized test environment.

Its purpose is to:

* Generate test traffic.
* Demonstrate abnormal traffic patterns.
* Allow traffic behavior to be monitored.
* Help evaluate the detection and mitigation mechanisms.

### Machine 3 – Server

Machine 3 acts as the target server.

Its responsibilities include:

* Receiving legitimate file uploads.
* Accepting network connections.
* Monitoring server resources.
* Observing incoming traffic.
* Applying the planned detection and mitigation mechanisms.

## 9. Overall Task Workflow

The planned workflow for the task is:

**Legitimate Client**
↓
**File Upload Request**
↓
**Server**

At the same time, controlled test traffic is generated:

**Traffic Generator**
↓
**Controlled Test Traffic**
↓
**Server**

The server-side monitoring is then used to observe the difference between normal and abnormal traffic.

**Traffic Generation → Monitoring → Detection → Mitigation → Verification**

## 10. Documentation and Preparation

As part of Day 14, I prepared the documentation required for the practical implementation of the task.

The preparation included:

* Understanding the role of each machine.
* Reviewing the communication flow.
* Identifying the required software and network configuration.
* Planning the monitoring parameters.
* Identifying the expected normal and abnormal traffic behavior.
* Preparing sections for recording experimental results and screenshots.
* Studying the concepts required before starting the practical test.

## 11. Key Learnings

The major concepts learned during the day were:

1. Difference between DoS and DDoS attacks.
2. Working principle of distributed traffic generation.
3. Major categories of DDoS attacks.
4. Network and application-level effects of excessive traffic.
5. Indicators used for DDoS detection.
6. Importance of traffic monitoring.
7. Rate limiting and traffic filtering.
8. Server resource monitoring.
9. Difference between legitimate and abnormal traffic.
10. Importance of controlled and authorized testing when studying network security.

## 12. Conclusion

Day 14 was focused on studying DDoS attacks in depth and preparing the documentation for the assigned practical task. I developed an understanding of DoS and DDoS concepts, attack categories, detection indicators, and common mitigation techniques.

I also studied the planned three-machine architecture consisting of a legitimate client, controlled traffic generator, and server. The practical implementation and testing will be carried out in the next stage, where the observed traffic, server behavior, detection results, and mitigation results can be documented.

**Day 14 Status:** Documentation and DDoS study completed. Practical implementation prepared for the next stage.
