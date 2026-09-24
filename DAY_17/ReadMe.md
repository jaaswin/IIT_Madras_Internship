# RCE-Based Controlled Distributed Traffic Demonstration and Detection (DDOS)

## Complete Detailed Project Report

---

# 1. Introduction

My project is a **controlled cybersecurity laboratory demonstration** that shows how a vulnerable web application can lead to **Remote Code Execution (RCE)** and how multiple controlled client machines can subsequently generate distributed HTTP traffic toward a target server.

The project is implemented using four virtual machines:

1. **Kali Linux** – attacker/controller/testing machine
2. **Ubuntu Target** – vulnerable Flask server and monitoring system
3. **Client 1** – controlled participating client
4. **Client 2** – controlled participating client

All four machines are connected through a private **VirtualBox Host-only network**.

The main concept of the project is:

```text
                 KALI
           Controller / Tester
           192.168.56.102
                  |
        +---------+---------+
        |                   |
        v                   v
    CLIENT 1            CLIENT 2
  .103 : 6000          .104 : 6000
        |                   |
        +---------+---------+
                  |
                  v
            UBUNTU TARGET
             .101 : 5000
                  |
          +-------+-------+
          |               |
          v               v
       RCE Endpoint    Monitoring
        /execute        + Alert
```

The project demonstrates the following overall sequence:

```text
Vulnerable Web Application
          ↓
         RCE
          ↓
Command Execution on Target
          ↓
Controlled Participating Clients
          ↓
Distributed HTTP Traffic
          ↓
Target Monitoring
          ↓
Abnormal Request Detection
          ↓
Alert
```

The important point is that **RCE and DDoS are not the same thing**.

RCE is demonstrated as the **initial compromise mechanism**.

The multiple clients are then used to demonstrate **distributed traffic behavior** in a controlled environment.

---

# 2. Main Objective of the Project

The main objective of my project is to demonstrate a complete cybersecurity scenario starting from a vulnerable application and ending with detection.

The project has several objectives.

### Objective 1 – Build an isolated security laboratory

I created four virtual machines using VirtualBox.

The machines communicate through a private Host-only network so that the experiment is separated from normal network traffic.

### Objective 2 – Implement an intentionally vulnerable application

I created a Flask application on Ubuntu.

The application contains an intentionally vulnerable `/execute` endpoint.

The endpoint accepts a command through an HTTP request and executes it on the Ubuntu server.

This is used only to demonstrate the concept of RCE inside the controlled lab.

### Objective 3 – Prove RCE

I did not simply claim that RCE exists.

I verified it using commands such as:

```bash
whoami
```

and:

```bash
hostname
```

The returned results showed that the commands were executed on the Ubuntu target.

### Objective 4 – Create participating clients

I configured:

* Client 1
* Client 2

Each client contains a small Flask lab agent.

The agent provides a controlled `/start-test` endpoint.

### Objective 5 – Generate controlled traffic

The clients run a bounded Python traffic-test script.

The script sends a fixed number of HTTP requests to the Ubuntu server.

### Objective 6 – Monitor the traffic

The Ubuntu server records:

* Source IP
* Requested URL
* Number of requests
* Time window

### Objective 7 – Generate an alert

If a client sends more than the configured number of requests within the monitoring window, the server prints:

```text
[ALERT] High request rate detected
```

This demonstrates the detection portion of the project.

---

# 3. Why I Used VirtualBox

I used **VirtualBox** because the project requires multiple separate machines.

Instead of buying four physical computers, I created four virtual machines.

VirtualBox allows each machine to behave like an independent computer with:

* its own operating system
* its own IP address
* its own network interface
* its own applications
* its own processes

Therefore, I can demonstrate communication between multiple machines while using only one physical Windows computer.

The virtual machines are:

```text
Windows Host
     |
     └── VirtualBox
          |
          +── Kali
          +── Ubuntu Target
          +── Client 1
          └── Client 2
```

This is particularly useful for cybersecurity labs because different machines can represent different roles.

---

# 4. Why I Used a Host-only Network

I used the VirtualBox **Host-only Adapter** for the laboratory communication.

The network used is:

```text
192.168.56.0/24
```

The machines have:

| Machine       | IP             |
| ------------- | -------------- |
| Kali          | 192.168.56.102 |
| Ubuntu Target | 192.168.56.101 |
| Client 1      | 192.168.56.103 |
| Client 2      | 192.168.56.104 |

The reason for using Host-only networking is isolation.

The communication becomes:

```text
Kali
 |
 +---- Ubuntu
 |
 +---- Client 1
 |
 +---- Client 2
```

The project traffic stays inside the lab network.

---

# 5. Why Some Machines Also Have NAT

For some machines, I used a second network adapter with NAT.

The reason is that Host-only networking provides communication between the lab machines but does not normally provide Internet access.

For example, Client 1 showed:

```text
10.0.3.15
```

This was its NAT interface.

Its project network address was:

```text
192.168.56.103
```

Therefore, these addresses have different purposes.

```text
10.0.3.15
     ↓
NAT / Internet access

192.168.56.103
     ↓
Private cybersecurity lab
```

This distinction is important when explaining the project.

---

# 6. Why I Used Kali Linux

Kali Linux is used as the **controller and testing machine**.

I use Kali to send HTTP requests to the Ubuntu target and clients.

For example:

```bash
curl http://192.168.56.101:5000/
```

and:

```bash
curl "http://192.168.56.101:5000/execute?cmd=whoami"
```

Kali is useful because it provides many cybersecurity and networking tools.

In this project, however, I mainly use it as the testing/controller machine.

The important point is:

> Kali is not the vulnerable server. Ubuntu is the vulnerable target.

---

# 7. Why I Used Ubuntu as the Target

Ubuntu is used as the target server.

The vulnerable Flask application runs on Ubuntu.

Its IP address is:

```text
192.168.56.101
```

The Flask server listens on:

```text
Port 5000
```

Therefore:

```text
192.168.56.101:5000
```

represents the target web application.

The Ubuntu machine performs two major roles:

1. Vulnerable RCE server
2. Traffic monitoring and alerting server

---

# 8. Why I Used Flask

I used **Flask** because it is a lightweight Python web framework.

For this project, I needed a simple HTTP server where I could control:

* endpoints
* HTTP parameters
* request processing
* command execution
* request monitoring
* logging

Flask makes this very simple.

For example:

```python
@app.route("/")
def home():
    return "Vulnerable RCE Lab Server"
```

This creates a simple HTTP endpoint.

I can test it with:

```bash
curl http://192.168.56.101:5000/
```

The server responds:

```text
Vulnerable RCE Lab Server
```

---

# 9. Ubuntu Project Structure

The Ubuntu project was created inside:

```text
~/rce-lab
```

The Python virtual environment is:

```text
~/rce-lab/venv
```

The basic structure is:

```text
rce-lab/
│
├── venv/
│
└── app.py
```

The virtual environment separates the project dependencies from the system Python environment.

I activate it using:

```bash
cd ~/rce-lab
source venv/bin/activate
```

After activation, the terminal shows:

```text
(venv)
```

This indicates that the virtual environment is active.

---

# 10. Why I Used a Python Virtual Environment

A virtual environment is used to isolate Python packages.

For example, Flask can be installed inside:

```text
rce-lab/venv
```

without modifying the entire operating system's Python environment.

This makes the project easier to manage.

The process is:

```bash
cd ~/rce-lab
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

The important distinction is:

> The virtual environment is for dependency management. It is not part of the RCE mechanism.

---

# 11. RCE Concept

RCE means:

> **Remote Code Execution**

It occurs when an attacker can cause a remote system to execute commands or code.

In my project, the vulnerable Flask application contains:

```text
/execute?cmd=...
```

The request contains a command.

For example:

```text
/execute?cmd=whoami
```

The Flask application reads the `cmd` parameter.

The application then executes it on the Ubuntu machine.

Conceptually:

```text
Kali
  |
  | HTTP request
  |
  | /execute?cmd=whoami
  ↓
Ubuntu Flask
  |
  | reads cmd
  ↓
subprocess
  |
  ↓
Ubuntu operating system
  |
  ↓
whoami
```

The important point is that the command is executed **on Ubuntu**, not on Kali.

---

# 12. Vulnerable RCE Code

The vulnerable endpoint is:

```python
@app.route("/execute")
def execute():
    command = request.args.get("cmd", "")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return f"""
    <h2>Command executed on Ubuntu</h2>
    <pre>{result.stdout}</pre>
    <pre>{result.stderr}</pre>
    """
```

There are several important components.

### `request.args.get()`

```python
command = request.args.get("cmd", "")
```

This retrieves the HTTP parameter.

For:

```text
?cmd=whoami
```

the value becomes:

```text
whoami
```

### `subprocess.run()`

```python
subprocess.run(...)
```

is used to execute the command from Python.

### `shell=True`

This tells Python to execute the command through the shell.

That is precisely what makes the endpoint intentionally unsafe when the input is untrusted.

---

# 13. Starting the Ubuntu Server

On Ubuntu:

```bash
cd ~/rce-lab
source venv/bin/activate
python3 app.py
```

The Flask application starts.

The application listens on:

```text
0.0.0.0:5000
```

`0.0.0.0` means Flask listens on the available network interfaces instead of only:

```text
127.0.0.1
```

Therefore, the Host-only clients can connect using:

```text
192.168.56.101:5000
```

---

# 14. First Test – Check Whether the Server Is Running

From Kali:

```bash
curl http://192.168.56.101:5000/
```

The server returns:

```text
Vulnerable RCE Lab Server
```

This proves:

```text
Kali → Ubuntu
```

communication is working.

It does not yet prove RCE.

It only proves that the Flask server is reachable.

---

# 15. RCE Proof Using `whoami`

I then test:

```bash
curl "http://192.168.56.101:5000/execute?cmd=whoami"
```

The server returns:

```text
rceuser
```

This is important because `whoami` identifies the account executing the command.

The command path is:

```text
Kali
  |
  | HTTP
  ↓
Ubuntu Flask
  |
  ↓
/execute
  |
  ↓
subprocess.run()
  |
  ↓
whoami
  |
  ↓
rceuser
```

Therefore, the command was executed by the Ubuntu application.

---

# 16. RCE Proof Using `hostname`

I then run:

```bash
curl "http://192.168.56.101:5000/execute?cmd=hostname"
```

The result is:

```text
ubuntu-target
```

This is stronger evidence because it identifies the machine where the command was executed.

The demonstration now proves:

```text
Remote HTTP Input
        ↓
Flask
        ↓
Command Execution
        ↓
Ubuntu Target
```

This is the core RCE proof in my project.

---

# 17. Why I Used `whoami` and `hostname`

I selected these commands because they are simple proof commands.

### `whoami`

Shows:

> Which user executed the command?

### `hostname`

Shows:

> Which machine executed the command?

Together they provide clear evidence.

For example:

```text
whoami
→ rceuser

hostname
→ ubuntu-target
```

This makes it easy to explain to the project reviewer:

> "The command was sent remotely from Kali, but the output identifies the user and hostname of the Ubuntu target, proving that command execution occurred on the target."

---

# 18. Handling Commands Containing Spaces

When a command contains spaces, normal URL syntax can cause problems.

For example:

```text
ip addr
```

contains a space.

I can use:

```bash
curl --get --data-urlencode "cmd=ip addr" \
http://192.168.56.101:5000/execute
```

This URL-encodes the command correctly.

This is a useful technical point when demonstrating the application.

---

# 19. Important Security Observation

The RCE implementation is deliberately vulnerable.

In a real application, this code should **not** be used:

```python
subprocess.run(command, shell=True)
```

when `command` comes directly from a user-controlled HTTP parameter.

A secure application would avoid arbitrary OS command execution or use a strict allowlist of predefined operations.

Therefore, in my project:

> The vulnerable endpoint exists specifically to demonstrate the RCE concept in an isolated laboratory.

---

# 20. Why I Added Monitoring

After demonstrating RCE, I wanted the project to show another important security concept:

> Detection.

Simply demonstrating an attack is incomplete from a cybersecurity perspective.

A security project should also show how suspicious behavior can be identified.

Therefore, I added request monitoring to the Flask server.

The monitor records:

```text
Source IP
Request path
Timestamp
Request count
```

---

# 21. Monitoring Window

I configured:

```python
WINDOW = 10
```

This means the application considers a:

```text
10-second window
```

For example:

```text
Time 0 → Request
Time 1 → Request
Time 2 → Request
...
Time 9 → Request
```

These requests are counted together.

Requests older than the window are removed.

---

# 22. Alert Threshold

I configured:

```python
ALERT_THRESHOLD = 10
```

Therefore, when the number of requests from a source exceeds 10 within the active 10-second window, the application prints:

```text
[ALERT] High request rate detected from <IP>
```

This provides a simple anomaly-detection mechanism.

---

# 23. How the Monitoring Works

The Flask application receives a request.

First it identifies the source IP:

```python
ip = request.remote_addr
```

Then it gets the current time:

```python
now = time.time()
```

It stores the timestamp.

Old timestamps are removed.

Then the current request count is calculated.

For example:

```text
192.168.56.103

Requests in 10 seconds:

1
2
3
4
5
...
10
11
```

When the count becomes greater than 10:

```text
[ALERT] High request rate detected from 192.168.56.103
```

---

# 24. Why Source IP Is Important

Source IP allows the server to identify where requests are coming from.

For example:

```text
192.168.56.103
```

is Client 1.

```text
192.168.56.104
```

is Client 2.

Therefore the target can distinguish the sources:

```text
Client 1 → .103
Client 2 → .104
```

This becomes important when demonstrating distributed traffic.

---

# 25. Why I Created Client 1 and Client 2

One machine generating traffic is not distributed traffic.

For example:

```text
Client 1
   |
   v
Ubuntu
```

has only one source.

But with two clients:

```text
Client 1 ─────┐
              |
              v
           Ubuntu
              ^
              |
Client 2 ─────┘
```

the target receives requests from multiple source IPs.

This demonstrates the basic idea of distributed traffic.

---

# 26. Client 1 Architecture

Client 1 has:

```text
IP:
192.168.56.103

Port:
6000
```

Its files are:

```text
rce-lab/
│
├── venv/
├── lab-agent.py
└── traffic-test.py
```

The client agent is a small Flask application.

---

# 27. Client 1 Lab Agent

The client agent contains:

```python
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "Client 1 Lab Agent"

@app.route("/start-test")
def start_test():
    subprocess.Popen(["python3", "traffic-test.py"])
    return "Controlled lab traffic started"

app.run(host="0.0.0.0", port=6000)
```

There are two important endpoints.

### `/`

Used to verify that the client agent is running.

### `/start-test`

Starts the controlled traffic test.

---

# 28. Why Client 1 Uses Port 6000

The Ubuntu target uses:

```text
5000
```

The client agents use:

```text
6000
```

This separates the services.

Therefore:

```text
Ubuntu:
192.168.56.101:5000
```

Client 1:

```text
192.168.56.103:6000
```

Client 2:

```text
192.168.56.104:6000
```

This makes the architecture easier to understand.

---

# 29. Starting Client 1

On Client 1:

```bash
cd ~/rce-lab
source venv/bin/activate
python3 lab-agent.py
```

Flask shows something similar to:

```text
Running on http://127.0.0.1:6000
Running on http://192.168.56.103:6000
```

Depending on the network interfaces, Flask may display another address such as:

```text
10.0.3.15
```

That is the NAT interface.

The important project IP is:

```text
192.168.56.103
```

---

# 30. Why Client 1 Uses a Virtual Environment

The virtual environment was created because Flask and Requests are Python packages.

The environment allows me to install these packages without changing the system Python installation.

When I run:

```bash
source venv/bin/activate
```

the prompt becomes:

```text
(venv)
```

This means the environment is active.

Then:

```bash
python3 lab-agent.py
```

uses the Python environment containing the required Flask package.

---

# 31. Testing Client 1

From Kali:

```bash
curl http://192.168.56.103:6000/
```

Expected response:

```text
Client 1 Lab Agent
```

This proves Client 1's Flask agent is running.

Then:

```bash
curl http://192.168.56.103:6000/start-test
```

Expected:

```text
Controlled lab traffic started
```

This launches the controlled traffic script.

---

# 32. Client 2

Client 2 performs the same role as Client 1.

Its IP is:

```text
192.168.56.104
```

Its Flask agent listens on:

```text
6000
```

Therefore:

```text
192.168.56.104:6000
```

is the Client 2 lab-agent service.

---

# 33. Client 2 Troubleshooting

I encountered an important issue on Client 2.

I initially tried:

```bash
cd ~/rce-lab
```

but received:

```text
No such file or directory
```

I also tried:

```bash
source venv/bin/activate
```

and received:

```text
No such file or directory
```

This happened because Client 2 did not have the same `rce-lab` directory structure as Client 1.

The files were actually present in the home directory:

```text
lab-agent.py
traffic-test.py
```

Therefore I did not need to run Ubuntu's `app.py` on Client 2.

I can simply run:

```bash
python3 lab-agent.py
```

from the directory containing the file.

This was an important troubleshooting step.

---

# 34. Difference Between `app.py` and `lab-agent.py`

This is very important for explaining the project.

### Ubuntu:

```text
app.py
```

Role:

```text
Vulnerable Target Server
```

IP:

```text
192.168.56.101
```

Port:

```text
5000
```

### Client 1:

```text
lab-agent.py
```

Role:

```text
Controlled Client
```

IP:

```text
192.168.56.103
```

Port:

```text
6000
```

### Client 2:

```text
lab-agent.py
```

Role:

```text
Controlled Client
```

IP:

```text
192.168.56.104
```

Port:

```text
6000
```

So:

```text
app.py
   ↓
Ubuntu Target

lab-agent.py
   ↓
Client 1 / Client 2
```

---

# 35. Traffic Test Script

The clients use:

```python
import requests
import time

TARGET = "http://192.168.56.101:5000/"

for i in range(20):
    try:
        r = requests.get(TARGET, timeout=2)
        print(i + 1, r.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(0.5)
```

This script has a fixed limit:

```text
20 requests
```

and a delay:

```text
0.5 seconds
```

between requests.

Therefore, the test is controlled and repeatable.

---

# 36. Why I Used a Bounded Traffic Test

I used a bounded script because the purpose of the project is to demonstrate:

```text
Multiple Sources
        ↓
Traffic
        ↓
Monitoring
        ↓
Detection
```

I do not need unlimited traffic.

The fixed number of requests makes the experiment:

* predictable
* repeatable
* easier to monitor
* safer
* easier to explain

---

# 37. How the Distributed Traffic Test Works

The complete process is:

```text
Kali
 |
 | /start-test
 |
 +--------> Client 1
 |             |
 |             | 20 requests
 |             v
 |         Ubuntu Target
 |
 +--------> Client 2
               |
               | 20 requests
               v
          Ubuntu Target
```

The target sees requests from:

```text
192.168.56.103
```

and:

```text
192.168.56.104
```

This provides multiple traffic sources.

---

# 38. What Happens on Ubuntu During the Test

The monitoring function prints entries similar to:

```text
[MONITOR] 192.168.56.103 -> / | requests in 10s: 1
```

Then:

```text
[MONITOR] 192.168.56.103 -> / | requests in 10s: 2
```

and so on.

As the number increases:

```text
[MONITOR] 192.168.56.103 -> / | requests in 10s: 10
```

When it exceeds the threshold:

```text
[ALERT] High request rate detected from 192.168.56.103
```

The same process can occur for:

```text
192.168.56.104
```

---

# 39. Complete Project Flow

The entire project can be explained as follows:

```text
                    KALI
               192.168.56.102
                       |
                       |
                Initial Testing
                       |
                       v
              UBUNTU TARGET
              192.168.56.101
                       |
                  /execute
                       |
                       v
                      RCE
                       |
             Command executes
                  on Ubuntu
                       |
          +------------+------------+
          |                         |
          v                         v
      CLIENT 1                 CLIENT 2
       .103                      .104
          |                         |
          | Controlled HTTP         |
          | traffic                 |
          +------------+------------+
                       |
                       v
                 Ubuntu Target
                       |
                       v
                 Request Monitor
                       |
                       v
               Threshold Check
                       |
                       v
                    ALERT
```

---

# 40. Why RCE Is Included in the Project

The RCE component demonstrates the initial compromise concept.

The logic is:

```text
Vulnerable Application
        ↓
Remote Input
        ↓
Command Execution
        ↓
Compromised Target
```

In a real attack scenario, command execution could potentially allow an attacker to perform many actions.

In my project, I use it only to demonstrate the vulnerability and establish the concept.

---

# 41. Why the Clients Are Included

The clients demonstrate the next part of the scenario.

Instead of only having:

```text
One machine → Target
```

I demonstrate:

```text
Client 1 ──┐
           ├──→ Target
Client 2 ──┘
```

This makes the traffic distributed across multiple source machines.

---

# 42. Why Monitoring Is Included

Without monitoring, the project would only show traffic generation.

With monitoring, I demonstrate a security detection mechanism:

```text
Traffic
   ↓
Observe
   ↓
Count
   ↓
Compare with threshold
   ↓
Alert
```

This gives the project a defensive cybersecurity component.

---

# 43. RCE vs DDoS

This is one of the most important explanations for my project.

### RCE

Remote Code Execution means:

> A remote party is able to cause code or operating-system commands to execute on a vulnerable system.

In my project:

```text
Kali
 ↓
HTTP /execute
 ↓
Ubuntu
 ↓
Command execution
```

### Distributed denial-of-service behavior

The traffic demonstration involves:

```text
Client 1
     \
      \
       → Ubuntu Target
      /
     /
Client 2
```

The clients generate requests from different source IP addresses.

Therefore:

> RCE is the demonstrated initial compromise mechanism, while the distributed traffic component demonstrates the behavior of multiple participating hosts sending traffic toward a target.

---

# 44. Important Difference From a Real Botnet

My project does not claim that the Flask RCE automatically creates a botnet.

A real botnet involves additional mechanisms such as:

* persistence
* command and control
* compromised hosts
* coordination
* malware
* propagation or initial infection mechanisms

I intentionally use controlled client VMs instead.

Therefore, the project demonstrates the **conceptual attack chain** without implementing self-spreading malware.

---

# 45. Why I Used Two Clients

One client demonstrates a single source.

Two clients allow me to demonstrate multiple sources.

For example:

```text
Source 1:
192.168.56.103

Source 2:
192.168.56.104
```

The target can distinguish these addresses.

This is useful for demonstrating distributed behavior.

---

# 46. Complete Testing Procedure

My final testing procedure is:

### Step 1 – Start Ubuntu

```bash
cd ~/rce-lab
source venv/bin/activate
python3 app.py
```

### Step 2 – Check target

From Kali:

```bash
curl http://192.168.56.101:5000/
```

### Step 3 – Prove RCE

```bash
curl "http://192.168.56.101:5000/execute?cmd=whoami"
```

Then:

```bash
curl "http://192.168.56.101:5000/execute?cmd=hostname"
```

### Step 4 – Start Client 1

```bash
cd ~/rce-lab
source venv/bin/activate
python3 lab-agent.py
```

### Step 5 – Test Client 1

From Kali:

```bash
curl http://192.168.56.103:6000/
```

Then:

```bash
curl http://192.168.56.103:6000/start-test
```

### Step 6 – Start Client 2

On Client 2:

```bash
python3 lab-agent.py
```

### Step 7 – Test Client 2

From Kali:

```bash
curl http://192.168.56.104:6000/
```

Then:

```bash
curl http://192.168.56.104:6000/start-test
```

### Step 8 – Watch Ubuntu

Observe:

```text
[MONITOR]
```

entries.

Then observe:

```text
[ALERT]
```

messages.

---

# 47. Evidence I Can Show to My In-Charge

I can show the following evidence during the project review.

### Evidence 1 – Network

Show:

```text
Kali       .102
Ubuntu     .101
Client 1   .103
Client 2   .104
```

### Evidence 2 – Target Server

Show:

```text
Vulnerable RCE Lab Server
```

### Evidence 3 – RCE

Show:

```text
whoami
→ rceuser
```

and:

```text
hostname
→ ubuntu-target
```

### Evidence 4 – Client 1

Show:

```text
Client 1 Lab Agent
```

### Evidence 5 – Client 2

Show:

```text
Client 2 Lab Agent
```

### Evidence 6 – Traffic

Show:

```text
1 200
2 200
3 200
...
```

### Evidence 7 – Monitoring

Show:

```text
[MONITOR] 192.168.56.103
[MONITOR] 192.168.56.104
```

### Evidence 8 – Alert

Show:

```text
[ALERT] High request rate detected
```

Together these provide evidence for the complete workflow.

---

# 48. Troubleshooting I Performed

Several practical problems occurred during implementation.

## Client 1 virtual environment problem

Initially Client 1 did not have the required project environment.

I created:

```bash
mkdir -p ~/rce-lab
cd ~/rce-lab
python3 -m venv venv
```

Then installed the required packages.

```bash
pip install flask requests
```

I verified them with:

```bash
python3 -c "import flask, requests; print('Ready')"
```

Output:

```text
Ready
```

---

# 49. Client 2 Connection Refused Problem

I tested:

```bash
curl http://192.168.56.104:6000/
```

and received:

```text
curl: (7) Failed to connect
```

This means the client was reachable at the network level only if the service was listening; in this case the Flask agent was not running.

The solution was:

```bash
python3 lab-agent.py
```

Then I tested again.

---

# 50. Client 2 Directory Problem

Client 2 showed:

```text
lab-agent.py
traffic-test.py
```

but:

```bash
cd ~/rce-lab
```

failed.

This means the files were in the home directory rather than:

```text
~/rce-lab
```

Therefore I should run:

```bash
python3 lab-agent.py
```

from the location containing the file.

This taught an important troubleshooting principle:

> Always check the actual file location before assuming that another VM has the same directory structure.

---

# 51. NAT IP vs Host-only IP Problem

Client 1 showed:

```text
10.0.3.15
```

while the project uses:

```text
192.168.56.103
```

This initially looks confusing.

The explanation is:

```text
10.0.3.15
     ↓
NAT interface

192.168.56.103
     ↓
Host-only interface
```

For communication between the four project machines, I use:

```text
192.168.56.x
```

---

# 52. Why Flask Shows 127.0.0.1

When Flask starts, it can show:

```text
http://127.0.0.1:6000
```

This means the service can be reached locally.

It also shows another interface because I configured:

```python
host="0.0.0.0"
```

Therefore it listens on all interfaces.

The project clients should use their Host-only addresses:

```text
Client 1 → 192.168.56.103
Client 2 → 192.168.56.104
```

---

# 53. Limitations of the Current Project

The current project is a demonstration rather than a production security system.

### Limitation 1

The RCE endpoint is intentionally vulnerable.

### Limitation 2

The monitoring data is stored in memory.

If Flask restarts, the request history disappears.

### Limitation 3

The alert system only uses a simple request-count threshold.

### Limitation 4

Only two clients are used.

### Limitation 5

The traffic is bounded and therefore does not represent Internet-scale DDoS.

### Limitation 6

The Flask development server is not intended for production.

---

# 54. Future Improvements

The project could be improved by adding:

### Database logging

Store requests in:

```text
SQLite
PostgreSQL
MySQL
```

### Centralized logging

Send events to a logging system or SIEM.

### Dashboard

Display:

```text
Source IP
Request count
Time
Endpoint
Alert status
```

### Better detection

Instead of only:

```text
> 10 requests
```

we could analyze:

* request rate
* request distribution
* endpoint frequency
* historical baseline
* source behavior

### Rate limiting

A production server could use:

```text
Flask-Limiter
Nginx
reverse proxy
firewall rules
```

to restrict excessive requests.

---

# 55. Why This Project Is a Cybersecurity Project

The project covers several cybersecurity concepts:

```text
Vulnerability
     ↓
RCE
     ↓
Initial Compromise
     ↓
Multiple Hosts
     ↓
Distributed Traffic
     ↓
Monitoring
     ↓
Detection
     ↓
Alert
```

Therefore, it demonstrates both:

### Offensive security concept

Understanding how a vulnerability can result in command execution.

### Defensive security concept

Monitoring abnormal traffic and generating alerts.

---

# 56. What I Actually Implemented

For my project explanation, I can say:

> "I created an isolated four-machine VirtualBox cybersecurity laboratory consisting of Kali, an Ubuntu target and two controlled client machines. I developed an intentionally vulnerable Flask application on Ubuntu to demonstrate Remote Code Execution. I verified the RCE using `whoami` and `hostname`, which showed execution on the Ubuntu target. I then configured Client 1 and Client 2 with Flask-based lab agents that launch a bounded HTTP traffic test. The Ubuntu server monitors incoming requests by source IP within a 10-second window and generates an alert when the request count exceeds the configured threshold. Finally, I tested the complete workflow and verified the traffic and alert messages from the target logs."

---

# 57. Short Explanation if My In-Charge Asks "What Is Your Project?"

I can answer:

> **"My project demonstrates RCE-based controlled distributed traffic and detection. I created a private VirtualBox network with Kali, Ubuntu, Client 1 and Client 2. The Ubuntu server contains an intentionally vulnerable Flask RCE endpoint. I prove the RCE by remotely executing `whoami` and `hostname`. I then use two controlled client machines to generate bounded HTTP traffic toward the Ubuntu server. The target monitors requests based on source IP and generates an alert when the request rate exceeds a threshold. So the project demonstrates initial compromise, distributed traffic generation and detection in an isolated cybersecurity lab."**

---

# 58. Final Project Flow

The entire project can finally be summarized as:

```text
┌───────────────────────────────┐
│       VirtualBox Lab          │
│      Private Network          │
│       192.168.56.0/24         │
└───────────────┬───────────────┘
                │
                ▼
        ┌───────────────┐
        │     KALI      │
        │     .102      │
        │ Controller    │
        └───────┬───────┘
                │
                │ HTTP Testing
                ▼
        ┌───────────────┐
        │ UBUNTU TARGET │
        │     .101      │
        │ Flask :5000   │
        └───────┬───────┘
                │
         ┌──────┴──────┐
         │             │
         ▼             ▼
       RCE          Monitoring
         │             │
         │             ▼
         │          Request
         │          Counting
         │             │
         ▼             ▼
    Command        Threshold
    Execution         Check
                       │
                       ▼
                     ALERT

       Controlled participating hosts
                │
       ┌────────┴────────┐
       ▼                 ▼
 CLIENT 1            CLIENT 2
   .103                 .104
   :6000                :6000
       │                 │
       └────────┬────────┘
                │
                ▼
        Bounded HTTP Traffic
                │
                ▼
          Ubuntu Target
```

## Final conclusion

The main achievement of the project is that I did not demonstrate only one isolated concept. I built a complete controlled workflow:

**VirtualBox network → vulnerable Flask application → RCE proof → controlled client machines → distributed HTTP traffic → source-IP monitoring → threshold detection → alert.**

The most important technical proof is the RCE output:

```text
whoami
→ rceuser
```

and:

```text
hostname
→ ubuntu-target
```

followed by the target observing traffic from:

```text
192.168.56.103
192.168.56.104
```

and producing:

```text
[ALERT] High request rate detected
```

