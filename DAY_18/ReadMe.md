# Controlled DDoS Detection and Mitigation – Project Update

## Project Overview

This repository contains the completed cybersecurity project for demonstrating **controlled distributed HTTP traffic, detection, and mitigation** in an isolated VirtualBox laboratory.

The original task demonstrated controlled HTTP traffic generation from multiple client machines toward an Ubuntu Flask target and implemented request monitoring with threshold-based alerting.

### Original Workflow

```text
Client 1 + Client 2
        ↓
Distributed HTTP Traffic
        ↓
Ubuntu Target
        ↓
Request Monitoring
        ↓
Threshold Detection
        ↓
ALERT
```

## Mitigation Introduced

As an extension to the completed task, I introduced a **mitigation mechanism** on the Ubuntu target.

The updated workflow is:

```text
Client 1 + Client 2
        ↓
Distributed HTTP Traffic
        ↓
Ubuntu Target
        ↓
Source-IP Monitoring
        ↓
Request Threshold Exceeded
        ↓
ALERT
        ↓
Temporary Source-IP Blocking
        ↓
HTTP 429
```

## Mitigation Implementation

The target monitors requests based on:

* **Source IP address**
* **Request count**
* **10-second monitoring window**
* **More than 10 requests as the threshold**

When a source exceeds the configured threshold:

1. The abnormal request rate is detected.
2. An alert is generated.
3. The source IP is temporarily blocked.
4. Further requests from the blocked source receive **HTTP 429 – Too Many Requests**.

### Example

```text
[MONITOR] 192.168.56.103 -> / | requests in 10s: 11
[ALERT] High request rate detected from 192.168.56.103
[MITIGATION] Temporarily blocking 192.168.56.103
```

A subsequent request from the blocked source receives:

```text
HTTP 429 Too Many Requests
```

## Lab Environment

| Machine    | Role                            | IP Address     |
| ---------- | ------------------------------- | -------------- |
| Kali Linux | Controller / Tester             | 192.168.56.102 |
| Ubuntu     | Target + Detection + Mitigation | 192.168.56.101 |
| Client 1   | Controlled Traffic Source       | 192.168.56.103 |
| Client 2   | Controlled Traffic Source       | 192.168.56.104 |

All machines operate within the private VirtualBox laboratory network.

## Project Enhancement

The main improvement introduced in this version is the transition from:

**Detection only**

to:

**Detection + Active Mitigation**

```text
BEFORE

Traffic → Monitoring → Alert


AFTER

Traffic → Monitoring → Alert → Block Source IP → HTTP 429
```

## Security Scope

This project is a **controlled laboratory demonstration**. The traffic is bounded and the environment is isolated. The mitigation is implemented at the application level on the Ubuntu Flask target.

The project also contains an intentionally vulnerable RCE demonstration as an additional security concept; RCE and DDoS are separate concepts.

## Final Result

The enhanced project demonstrates:

**Controlled Distributed HTTP Traffic → Detection → Alerting → Source-IP Mitigation → HTTP 429 Response**
