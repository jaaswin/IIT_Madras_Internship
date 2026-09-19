

# DAY 13 – FULL PROJECT REPORT

## Controlled DDoS Detection and Secure File Upload Lab

---

## 1. Project Overview

This project implements a controlled three-machine Docker environment for demonstrating:

* Secure file-upload communication
* Network/application request monitoring
* Abnormal traffic detection
* IDS-style alert generation
* Rate limiting
* Excessive traffic mitigation
* Verification of legitimate traffic after mitigation

The complete environment consists of three Docker containers:

**Machine 1 – Legitimate Client**

Machine 1 represents a normal user/client. It uploads a legitimate file to the server.

**Machine 2 – Traffic Generator**

Machine 2 generates controlled repeated upload requests to simulate excessive application-layer traffic.

**Machine 3 – Server + IDS**

Machine 3 hosts the Flask file-upload service. It monitors incoming upload requests, detects abnormal request patterns, generates alerts, and applies rate limiting to excessive traffic.

The containers communicate through a private Docker bridge network.

---

# 2. Project Objective

The main objective of this project is to demonstrate how a server can detect and mitigate excessive upload traffic while continuing to serve legitimate clients.

The project has the following objectives:

1. Create three isolated Docker machines.
2. Establish communication between the machines.
3. Create a file-upload server using Flask.
4. Allow legitimate clients to upload files.
5. Monitor incoming upload requests.
6. Identify abnormal upload behavior.
7. Generate an IDS alert when abnormal activity is detected.
8. Apply rate limiting to excessive requests.
9. Return HTTP 429 when the request limit is exceeded.
10. Verify that legitimate uploads continue after mitigation.

---

# 3. Problem Statement

A file-upload service can be affected by excessive requests.

For example, if a client continuously sends upload requests:

```text
Client
   |
   | Request
   | Request
   | Request
   | Request
   | Request
   | Request
   | ...
   v
Server
```

The server may have to repeatedly process:

* HTTP requests
* File uploads
* File storage
* CPU operations
* Memory usage
* Network traffic
* Disk I/O

If excessive traffic continues, the service may become slower or unavailable.

Therefore, the server needs mechanisms to:

```text
Monitor
   ↓
Detect
   ↓
Alert
   ↓
Mitigate
   ↓
Verify
```

This project demonstrates that complete workflow in a controlled Docker environment.

---

# 4. Important Security Classification

This project uses **one traffic-generator container**.

Therefore, technically, the experiment is a:

**Controlled excessive-traffic / DoS-style simulation**

rather than a fully distributed DDoS attack.

A true DDoS demonstration would normally use multiple independent traffic sources.

For example:

```text
Machine 2
     |
Machine 4
     |
Machine 5
     |
     +---------> Machine 3
     |
Machine 6
```

However, the current implementation demonstrates the important concepts of:

* Traffic monitoring
* Abnormal behavior detection
* Alert generation
* Rate limiting
* Traffic mitigation

All traffic generation is performed inside the private Docker laboratory.

---

# 5. System Architecture

The system architecture is:

```text
                 PRIVATE DOCKER NETWORK
                       ddos-lab
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     MACHINE 1         MACHINE 2         MACHINE 3
     Legitimate        Traffic           Server + IDS
     Client            Generator         File Upload
          |                |                |
          |                |                |
          +----------------+----------------+
                           |
                    Request Monitoring
                           |
                    IDS Alert Detection
                           |
                     Rate Limiting
                           |
                  Excess Traffic Block
```

---

# 6. Machine 1 – Legitimate Client

Machine 1 represents a normal client.

Its main purpose is to demonstrate legitimate communication with the server.

### Responsibilities

Machine 1:

* Creates a legitimate file.
* Sends the file to Machine 3.
* Receives a successful response.
* Verifies that the file was uploaded.
* Tests the server again after mitigation.

The container name is:

```text
machine1-client
```

The image used is:

```text
python:3.12-slim
```

---

# 7. Machine 2 – Traffic Generator

Machine 2 generates controlled repeated upload requests.

The container name is:

```text
machine2-attacker
```

The name represents its role in the demonstration, but the traffic is generated only against the user's own private Docker server.

### Responsibilities

Machine 2:

* Creates a test file.
* Sends repeated upload requests.
* Generates excessive application-layer traffic.
* Tests the server's detection mechanism.
* Tests the server's rate-limiting mechanism.

The image used is:

```text
python:3.12-slim
```

---

# 8. Machine 3 – Server + IDS

Machine 3 is the most important component.

It performs several functions:

```text
              MACHINE 3
                  |
       +----------+----------+
       |          |          |
       v          v          v
     Flask      IDS       Rate Limit
     Server   Monitoring   Mitigation
       |          |          |
       +----------+----------+
                  |
             File Upload
```

Machine 3:

* Hosts the Flask application.
* Provides the `/upload` endpoint.
* Stores uploaded files.
* Monitors requests.
* Tracks client IP addresses.
* Detects abnormal request patterns.
* Generates alerts.
* Applies rate limiting.
* Blocks excessive requests.

---

# 9. Technologies Used

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Docker                | Containerization                |
| Docker Compose        | Container orchestration         |
| Python 3.12           | Application/runtime environment |
| Flask                 | Web server and file-upload API  |
| Flask-Limiter         | Rate limiting                   |
| Docker Bridge Network | Private container communication |
| curl                  | HTTP testing                    |
| Linux                 | Container operating environment |

---

# 10. Why Docker Is Used

Docker is used to create isolated environments for the three machines.

Without Docker, we would need multiple physical or virtual machines.

With Docker:

```text
Computer
   |
   +--- Machine 1 Container
   |
   +--- Machine 2 Container
   |
   +--- Machine 3 Container
```

### Advantages

Docker provides:

* Isolation
* Reproducibility
* Easy setup
* Easy cleanup
* Private networking
* Lightweight environments
* Consistent testing

It also makes the project easy to demonstrate on another computer.

---

# 11. Why Docker Compose Is Used

Docker Compose allows all three containers and the network to be defined in one configuration file.

The project uses:

```text
docker-compose.yml
```

Instead of manually creating each container, we can use:

```bash
docker compose up -d --build
```

This automatically:

1. Builds Machine 3.
2. Creates Machine 1.
3. Creates Machine 2.
4. Creates the Docker network.
5. Connects the containers.
6. Starts all services.

---

# 12. Docker Compose Architecture

The configuration contains three services:

```text
services:
    machine3
    machine1
    machine2
```

And one network:

```text
ddos-lab
```

The network uses:

```text
driver: bridge
```

---

# 13. Why a Docker Bridge Network Is Used

The containers need to communicate with each other.

The bridge network provides a private network:

```text
Machine 1
    |
    +------ ddos-lab ------+
    |                      |
Machine 2              Machine 3
```

The observed network configuration was:

```text
Network: ddos-file-upload-lab_ddos-lab
Driver: bridge
Subnet: 172.18.0.0/16
Gateway: 172.18.0.1
```

The containers were observed with addresses such as:

```text
Machine 1 → 172.18.0.2
Machine 2 → 172.18.0.3
Machine 3 → 172.18.0.4
```

These IP addresses can change when containers are recreated.

Therefore, the project does **not** depend on hard-coded container IP addresses.

Instead, it uses:

```text
machine3-server
```

Docker automatically resolves that service name.

---

# 14. Why Docker DNS Is Used

Machine 1 and Machine 2 communicate with Machine 3 using:

```text
http://machine3-server:5000
```

rather than:

```text
http://172.18.0.4:5000
```

This is better because the container IP may change.

Docker provides internal DNS.

Therefore:

```text
machine3-server
       ↓
Docker DNS
       ↓
Current Machine 3 IP
```

---

# 15. Project Structure

The final project structure is:

```text
DAY_13/
│
├── .gitignore
├── ReadMe.md
├── docker-compose.yml
│
└── server/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

---

# 16. Server Application

The server is developed using Python Flask.

The server provides:

```text
/
```

and:

```text
/upload
```

The `/upload` endpoint accepts HTTP POST requests.

---

# 17. Why Flask Is Used

Flask is used because it is:

* Lightweight
* Simple
* Easy to configure
* Suitable for REST APIs
* Easy to run inside Docker
* Suitable for demonstrating HTTP requests

For this project, Flask provides the basic HTTP server required for the experiment.

---

# 18. File Upload Process

The upload process is:

```text
Client
   |
   | POST /upload
   |
   v
Flask Server
   |
   | Check file
   |
   | Save file
   |
   v
/ app / uploads
```

The server checks:

1. Whether a file was provided.
2. Whether the filename exists.
3. Saves the file.
4. Generates an upload log.
5. Returns a success response.

---

# 19. Upload Directory

Uploaded files are stored in:

```text
/app/uploads
```

The application creates this directory automatically:

```python
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

This ensures that the directory exists before the server attempts to save files.

---

# 20. IDS Monitoring

The project contains a simple IDS-style monitoring mechanism.

The server maintains:

```python
request_times = {}
```

This dictionary stores request timestamps for each client IP.

The monitoring configuration is:

```text
ALERT_THRESHOLD = 5
MONITOR_WINDOW = 60
```

Meaning:

```text
5 requests
within
60 seconds
```

will generate an alert.

---

# 21. Why Request Monitoring Is Used

Without monitoring, the server would simply process requests.

For example:

```text
Request
Request
Request
Request
Request
Request
Request
```

The administrator would not have an immediate indication that the traffic pattern is abnormal.

Monitoring provides visibility.

The server produces logs such as:

```text
[MONITOR] Upload request #1
[MONITOR] Upload request #2
[MONITOR] Upload request #3
```

This helps identify request behavior.

---

# 22. Why a 60-Second Window Is Used

The system uses a 60-second monitoring window.

This means the IDS focuses on **recent activity**.

For example:

```text
10:00:01 → Request
10:00:10 → Request
10:00:20 → Request
10:00:30 → Request
10:00:40 → Request
```

Five requests within the same 60-second period can trigger the alert.

Older requests are removed from the tracking list.

This is more useful than maintaining a permanent counter because the detection is based on the current request rate.

---

# 23. IDS Alert Threshold

The configured threshold is:

```text
5 requests
```

When the client reaches five upload requests within 60 seconds, the server prints:

```text
[ALERT] Abnormal upload activity detected
from 172.18.0.3
(5 requests in 60 seconds)
```

The exact IP can differ between runs.

---

# 24. Why an IDS Alert Is Needed

The IDS alert provides an indication that the server has detected an abnormal pattern.

The process is:

```text
Incoming Request
       ↓
Request Count
       ↓
Compare with Threshold
       ↓
Threshold Reached?
       ↓
      YES
       ↓
Generate Alert
```

This separates **detection** from **mitigation**.

---

# 25. Rate Limiting

The project uses Flask-Limiter.

The configured limit is:

```text
5 uploads per minute per client
```

The implementation uses the client IP as the rate-limit key.

Therefore:

```text
Client A → 5 requests/minute
Client B → 5 requests/minute
```

Each client is evaluated separately.

---

# 26. Why Rate Limiting Is Used

IDS detection alone does not stop the traffic.

For example:

```text
IDS:
"Abnormal traffic detected!"
```

But if the server continues accepting requests, the problem remains.

Rate limiting provides an automatic response:

```text
Detect
  ↓
Limit
  ↓
Block excessive requests
```

This reduces the amount of traffic processed by the upload endpoint.

---

# 27. HTTP 429

When the rate limit is exceeded, the server returns:

```text
HTTP 429
```

HTTP 429 means:

```text
Too Many Requests
```

The application returns:

```json
{
    "status": "blocked",
    "message": "Rate limit exceeded"
}
```

---

# 28. Why HTTP 429 Is Used

HTTP 429 is specifically designed to indicate that the client has sent too many requests in a given period.

Therefore, it clearly communicates:

```text
Client
  ↓
Too many requests
  ↓
Server
  ↓
HTTP 429
```

---

# 29. Complete Detection and Mitigation Flow

The complete process is:

```text
             Incoming Request
                    |
                    v
            Request Monitoring
                    |
                    v
            Count Recent Requests
                    |
                    v
        Is Threshold Reached?
             /          \
           No            Yes
           |              |
           v              v
      Continue        IDS Alert
                          |
                          v
                    Rate Limiting
                          |
                          v
                  Limit Exceeded?
                    /        \
                  No          Yes
                  |            |
                  v            v
             HTTP 200       HTTP 429
                               |
                               v
                         Traffic Blocked
```

---

# 30. Dockerfile

The server uses:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /app/uploads

EXPOSE 5000

CMD ["python", "-u", "app.py"]
```

---

# 31. Why `python:3.12-slim` Is Used

The Python slim image provides Python without many unnecessary operating-system packages.

Benefits:

* Smaller image
* Faster deployment
* Reduced unnecessary components
* Suitable for the Flask application

---

# 32. Why Port 5000 Is Used

Flask runs inside the container on:

```text
5000
```

The Docker Compose file maps:

```text
8080:5000
```

Meaning:

```text
Windows Host
     |
     | Port 8080
     v
Docker Container
     |
     | Port 5000
     v
Flask
```

Therefore, from Windows:

```text
http://localhost:8080
```

can reach the Flask server.

Inside the Docker network:

```text
http://machine3-server:5000
```

is used.

---

# 33. Why `python -u` Is Used

The Dockerfile uses:

```text
python -u app.py
```

The `-u` option makes Python output unbuffered.

This is useful because IDS logs should appear immediately when viewing:

```bash
docker logs -f machine3-server
```

Without immediate output, logs can sometimes appear delayed because of output buffering.

---

# 34. Legitimate File Upload Test

Machine 1 creates:

```text
legitimate.txt
```

with content:

```text
This is a legitimate file from Machine 1
```

The upload command is:

```bash
curl -F "file=@legitimate.txt" \
http://machine3-server:5000/upload
```

The server returns:

```json
{
    "message": "File uploaded successfully",
    "status": "success"
}
```

The file is then verified inside Machine 3:

```bash
ls -l /app/uploads
```

and:

```bash
cat /app/uploads/legitimate.txt
```

---

# 35. Controlled Excessive Traffic Test

Machine 2 creates:

```text
attack.txt
```

with controlled test content.

Then it sends repeated requests:

```bash
for i in {1..10}; do
  echo "Request $i"
  curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" \
  -F "file=@attack.txt" \
  http://machine3-server:5000/upload
done
```

---

# 36. Test Results

The observed results were:

```text
Request 1 → HTTP 200
Request 2 → HTTP 200
Request 3 → HTTP 200
Request 4 → HTTP 200
Request 5 → HTTP 200

Request 6 → HTTP 429
Request 7 → HTTP 429
Request 8 → HTTP 429
Request 9 → HTTP 429
Request 10 → HTTP 429
```

This demonstrates the rate-limiting mechanism.

---

# 37. IDS Log Results

Machine 3 generated logs such as:

```text
[MONITOR] Upload request #5 from 172.18.0.2

[ALERT] Abnormal upload activity detected
from 172.18.0.2
(5 requests in 60 seconds)
```

This proves that the monitoring mechanism detected the configured abnormal pattern.

---

# 38. Mitigation Logs

After the rate limit was exceeded:

```text
[MONITOR] Upload request #6 from 172.18.0.2

[MITIGATION] Excessive traffic blocked
from 172.18.0.2
```

Further requests continued to receive HTTP 429.

This proves that the mitigation mechanism was activated.

---

# 39. Final Legitimate Traffic Verification

After Machine 2's excessive traffic was blocked, Machine 1 performed another legitimate upload.

Command:

```bash
curl -s -F "file=@legitimate.txt" \
http://machine3-server:5000/upload
```

Response:

```json
{
    "message": "File uploaded successfully",
    "status": "success"
}
```

This is an important part of the project.

It proves:

```text
Excessive Traffic
       ↓
Detected
       ↓
Blocked
       ↓
Legitimate Client
       ↓
Still Works
```

---

# 40. Why Final Verification Is Important

Suppose the mitigation simply blocked all traffic.

Then:

```text
Attacker → Blocked
Legitimate Client → Also Blocked
```

That would not be desirable.

The purpose of rate limiting is to control excessive traffic while maintaining normal service for legitimate users.

Therefore, testing Machine 1 after mitigation verifies the intended behavior.

---

# 41. Monitoring the Server

Machine 3 logs can be viewed using:

```bash
docker logs -f machine3-server
```

The logs contain three important categories.

### Monitoring

```text
[MONITOR]
```

Shows incoming upload activity.

### Alert

```text
[ALERT]
```

Shows that the configured abnormal threshold was reached.

### Mitigation

```text
[MITIGATION]
```

Shows that excessive traffic was blocked.

---

# 42. Complete Demonstration

The complete demonstration can be presented as:

```text
START DOCKER
     ↓
Create 3 Containers
     ↓
Create Private Network
     ↓
Start Flask Server
     ↓
Machine 1 Uploads Legitimate File
     ↓
HTTP 200
     ↓
Machine 2 Generates Controlled Excessive Traffic
     ↓
Server Monitors Requests
     ↓
5 Requests Reached
     ↓
IDS Alert Generated
     ↓
Rate Limit Exceeded
     ↓
HTTP 429
     ↓
Excessive Traffic Blocked
     ↓
Machine 1 Uploads Again
     ↓
HTTP 200
```

---

# 43. Why This Project Is Useful

This project demonstrates several real-world cybersecurity concepts in a simple environment.

It shows how security systems can combine:

```text
Visibility
+
Detection
+
Alerting
+
Mitigation
+
Verification
```

Instead of implementing only one security mechanism, the project demonstrates the complete lifecycle.

---

# 44. Security Concepts Demonstrated

### 44.1 Denial of Service

A service can become unavailable or degraded when excessive requests consume its resources.

### 44.2 Distributed Denial of Service

DDoS is the distributed form where traffic originates from multiple sources.

The current project simulates the concepts using one controlled traffic-generator container.

### 44.3 Intrusion Detection System

The IDS observes traffic behavior and identifies activity matching a configured abnormal pattern.

### 44.4 Rate Limiting

Rate limiting controls the number of requests allowed during a specified period.

### 44.5 Traffic Mitigation

Mitigation is the response used to reduce the effect of abnormal traffic.

### 44.6 Application-Layer Protection

The project protects an HTTP upload endpoint, so the demonstration operates at the application layer.

---

# 45. Limitations

The current project has some limitations.

### 1. Single Traffic Generator

Only one traffic-generator container is used.

A real distributed demonstration would use multiple traffic sources.

### 2. Simple Detection Rule

The IDS uses a fixed threshold:

```text
5 requests / 60 seconds
```

It does not use advanced behavioral analysis or machine learning.

### 3. In-Memory Rate-Limit Storage

Flask-Limiter uses in-memory tracking in the current implementation.

For a production multi-instance application, a shared storage backend would normally be used.

### 4. Basic File Handling

A production upload service should additionally implement:

* Filename sanitization
* File type validation
* File size limits
* Authentication
* Authorization
* Malware scanning
* Secure storage

### 5. Not a Production DDoS Protection Platform

The project demonstrates the concepts in a controlled lab. It is not intended to replace enterprise DDoS protection systems.

---

# 46. Future Improvements

The project can be improved by adding:

### Multiple Traffic Sources

```text
Machine 2
Machine 4
Machine 5
Machine 6
      |
      v
Machine 3
```

This would provide a more distributed traffic simulation.

### Redis Rate-Limit Storage

Redis could provide shared rate-limit information when multiple server instances are used.

### Dashboard

A monitoring dashboard could display:

* Request count
* Blocked requests
* Client IP
* Alerts
* Upload activity

### Authentication

Require users to authenticate before uploading files.

### File Validation

Validate:

* File extension
* MIME type
* File size
* Filename

### Advanced IDS

The system could analyze:

* Request frequency
* Request size
* User behavior
* IP reputation
* Request patterns

### Automated Notifications

Alerts could be sent through an authorized notification system.

---

# 47. GitHub Repository

The project is organized in the internship repository as:

```text
IIT_Madras_Internship/
│
├── DAY_01/
├── DAY_02/
├── DAY_03/
├── ...
├── DAY_12/
│
└── DAY_13/
    ├── .gitignore
    ├── ReadMe.md
    ├── docker-compose.yml
    │
    └── server/
        ├── app.py
        ├── Dockerfile
        └── requirements.txt
```

This structure keeps the Day 13 project together with the other internship work.

---

# 48. Main Commands Used

### Start the project

```bash
docker compose up -d --build
```

### Check containers

```bash
docker ps
```

### Enter Machine 1

```bash
docker exec -it machine1-client bash
```

### Enter Machine 2

```bash
docker exec -it machine2-attacker bash
```

### View Machine 3 logs

```bash
docker logs -f machine3-server
```

### Check Docker network

```bash
docker network inspect ddos-file-upload-lab_ddos-lab
```

### Stop the environment

```bash
docker compose down
```

---

# 49. Expected Viva Questions and Answers

### Q1. Why did you use Docker?

Docker allows me to create three isolated machines on one computer and connect them through a controlled private network.

### Q2. Why did you use Docker Compose?

Docker Compose allows me to define all three containers and the network in a single configuration file and start them together.

### Q3. Why did you use Flask?

Flask provides a lightweight HTTP server and makes it easy to implement the file-upload API.

### Q4. Why did you use Flask-Limiter?

Flask-Limiter provides rate limiting so that a client cannot continuously send unlimited requests.

### Q5. What happens when the limit is exceeded?

The server returns HTTP 429, which means Too Many Requests.

### Q6. What is the IDS doing?

The IDS monitors upload requests from each client IP and generates an alert when five requests occur within 60 seconds.

### Q7. Why do you need both IDS and rate limiting?

IDS provides detection and alerting, while rate limiting provides automated mitigation.

### Q8. Why are you using client IP addresses?

The IP address provides a simple way to identify the source of requests and apply monitoring and rate limits per client.

### Q9. Why are you using a private Docker network?

It isolates the experiment and allows the three containers to communicate safely within the controlled lab.

### Q10. Why do you use `machine3-server` instead of an IP address?

Docker provides internal DNS, so the service name remains usable even if the container's IP changes.

### Q11. What does HTTP 429 mean?

HTTP 429 means the client has sent too many requests in the configured time period.

### Q12. How did you verify mitigation?

I generated excessive traffic from Machine 2, observed HTTP 429 responses and mitigation logs, and then uploaded a legitimate file from Machine 1. The legitimate upload still returned HTTP 200.

### Q13. Is this a real DDoS attack?

It is a controlled excessive-traffic/DoS-style simulation using one traffic-generator container. A fully distributed DDoS laboratory would require multiple independent traffic sources.

---

# 50. Final Conclusion

This project successfully demonstrates a controlled security environment for detecting and mitigating excessive HTTP file-upload traffic.

The complete workflow is:

```text
Legitimate Client
       ↓
File Upload
       ↓
Server
       ↓
Request Monitoring
       ↓
Abnormal Traffic
       ↓
IDS Alert
       ↓
Rate Limiting
       ↓
HTTP 429
       ↓
Excessive Traffic Blocked
       ↓
Legitimate Client Tested
       ↓
Upload Successful
```

