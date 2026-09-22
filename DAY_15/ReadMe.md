# DAY 15 – RCE, DDoS Detection and Mitigation

**Organization:** IIT Madras – Computer Centre
**Intern:** Jayaaswin M.

## 1. Introduction

On Day 15 of the internship, the previously assigned DDoS-related task was updated to include the concept of **Remote Code Execution (RCE)**. The revised task combines the study of RCE, DDoS activity, detection, and mitigation in a controlled network environment.

I studied the fundamentals of RCE and continued my in-depth study of DDoS attacks and mitigation techniques. I also reviewed how the three-machine environment can be used to perform the assigned security task in a controlled and authorized setup.

## 2. Task Update

The initial task focused on demonstrating DDoS activity and mitigation using three machines.

The task was later updated to include **RCE** as an additional security concept.

The revised task focuses on:

**RCE + DDoS Detection + DDoS Mitigation**

The objective is to understand how different security issues can affect a networked server and how monitoring and defensive mechanisms can be used to identify and control abnormal activity.

## 3. Remote Code Execution (RCE)

**Remote Code Execution (RCE)** is a security vulnerability or attack condition that allows an unauthorized remote party to cause a system to execute commands or code.

RCE can occur when an application or service improperly handles untrusted input, allowing an attacker to influence what the target system executes.

The general concept is:

**Remote Source → Vulnerable Service/Application → Untrusted Input → Code/Command Execution**

RCE can potentially affect the confidentiality, integrity, and availability of a system, depending on the privileges and access available to the executed process.

## 4. RCE Study

During the study, I focused on the following concepts:

* Meaning and working principle of RCE.
* How vulnerable applications may allow remote code execution.
* Role of untrusted input in security vulnerabilities.
* Difference between normal application requests and malicious input.
* Importance of input validation and secure application design.
* Principle of least privilege.
* Monitoring and logging of suspicious activities.
* Importance of patching and updating vulnerable services.

The practical work will be performed only within the authorized internship environment.

## 5. DDoS Study

I continued studying **Distributed Denial-of-Service (DDoS)** attacks.

A DDoS attack involves multiple sources generating traffic or requests toward a target system. Excessive traffic can consume network or server resources and may affect service availability.

The basic flow is:

**Multiple Sources → Network → Target Server → Resource Consumption → Service Degradation**

The study focused on understanding how abnormal traffic differs from normal traffic and how these differences can be monitored.

## 6. DDoS Detection

I studied different parameters that can be monitored to identify abnormal traffic conditions:

* Traffic volume
* Packet rate
* Number of connections
* Number of requests
* Source addresses
* Bandwidth utilization
* CPU utilization
* Memory utilization
* Packet drops
* Server response time

Monitoring these parameters can help identify unusual changes in network and server behavior.

## 7. DDoS Mitigation

I studied several defensive techniques that can be used to reduce the impact of abnormal traffic.

### Rate Limiting

Restricting the number of requests or connections accepted during a specific time period.

### Traffic Filtering

Filtering unwanted traffic according to defined security rules.

### Firewall Controls

Using firewall policies to control permitted and blocked traffic.

### Connection Limiting

Limiting excessive simultaneous connections to protect server resources.

### Monitoring and Alerting

Monitoring network and system parameters to identify abnormal activity and generate alerts.

## 8. Three-Machine Environment

The practical task uses a controlled three-machine architecture.

### Machine 1 – Legitimate Client

The legitimate client represents a normal user and is used to generate legitimate requests or perform file-upload communication with the server.

### Machine 2 – Controlled Testing Machine

This machine is used to perform the authorized security testing required for the task, including controlled traffic generation and testing of the assigned security concepts.

### Machine 3 – Server

The server provides the required service and acts as the system being monitored during the testing process.

The server-side activity will be observed to identify changes in traffic, resource utilization, and application behavior.

## 9. Updated Task Workflow

The planned workflow for the revised task is:

**Three-Machine Setup**
↓
**Establish Normal Communication**
↓
**Perform Authorized Security Testing**
↓
**RCE-Related Testing / Observation**
↓
**DDoS Traffic Testing**
↓
**Monitor Server and Network Behavior**
↓
**Detect Abnormal Activity**
↓
**Apply Mitigation**
↓
**Verify Service Recovery and Normal Traffic**

## 10. Security Considerations

During the study, I understood that both RCE and DDoS testing must be performed only in an authorized and isolated environment.

Important security practices include:

* Using systems specifically provided for testing.
* Avoiding unauthorized targets.
* Keeping testing within defined limits.
* Monitoring the test environment continuously.
* Using controlled traffic rather than uncontrolled attack traffic.
* Recording observations and results.
* Applying mitigation after identifying abnormal behavior.

## 11. Key Learnings

The major concepts learned during Day 15 were:

1. Remote Code Execution and its basic working principle.
2. How vulnerable services can potentially allow remote code execution.
3. Importance of input validation and secure application design.
4. DDoS attack fundamentals.
5. Difference between normal and abnormal network traffic.
6. DDoS detection parameters.
7. Basic DDoS mitigation techniques.
8. Importance of server and network monitoring.
9. Three-machine security-testing architecture.
10. Importance of performing security experiments in a controlled and authorized environment.

## 12. Conclusion

Day 15 focused on the updated network-security task involving **RCE, DDoS detection, and DDoS mitigation**. I studied the fundamentals of Remote Code Execution and continued my detailed study of DDoS attacks, detection indicators, and mitigation techniques.

I also reviewed the three-machine environment and prepared the workflow required for the practical implementation. The next stage will focus on carrying out the authorized testing, monitoring the system behavior, implementing the required mitigation mechanisms, and documenting the observations and results.

**Day 15 Status:** RCE, DDoS detection, and mitigation concepts studied; updated task requirements reviewed; practical implementation prepared.
