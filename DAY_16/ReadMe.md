# RCE Vulnerability Demonstration Lab — Complete Project Report

## 1. Project Title

**Controlled Remote Code Execution (RCE) Demonstration Using Kali Linux and Ubuntu Server**

---

## 2. Project Overview

This project demonstrates how a **Remote Code Execution (RCE)** vulnerability can allow an attacker-controlled request to cause code or a command to execute on a remote server.

A completely isolated VirtualBox laboratory was created using two virtual machines:

* **Kali Linux** — attacker/testing machine
* **Ubuntu Server** — vulnerable target machine

A Flask web application was deployed on the Ubuntu server. The application contained a deliberately controlled execution point. A request originating from Kali was sent to the Flask application, and the Ubuntu server performed a real server-side operation (`hostname`).

The purpose was to demonstrate the **actual execution flow**, rather than displaying a fake `"RCE successful"` message.

---

# 3. Project Objective

The main objectives were:

1. Create an isolated attacker-target environment.
2. Configure Kali Linux as the testing machine.
3. Configure Ubuntu Server as the target.
4. Establish network communication between both machines.
5. Install Python and Flask on Ubuntu.
6. Develop a controlled vulnerable Flask application.
7. Run the Flask application on the Ubuntu server.
8. Access the application remotely from Kali.
9. Demonstrate controlled server-side command execution.
10. Verify that the execution occurred on the Ubuntu machine.

---

# 4. What is RCE?

**Remote Code Execution (RCE)** is a security vulnerability where an attacker can cause code or commands to execute on a remote system through a network-accessible application.

Normally, a web application should process user input safely.

For example:

```text
User
 ↓
Web Application
 ↓
Validate input
 ↓
Perform allowed operation
```

With an RCE vulnerability, attacker-controlled input can reach an execution mechanism:

```text
Attacker
   ↓
Malicious/controlled request
   ↓
Vulnerable application
   ↓
Execution mechanism
   ↓
Operating system
   ↓
Command executes on server
```

The important point is that **the execution occurs on the server**, not on the attacker's computer.

---

# 5. Lab Architecture

The project used two VirtualBox virtual machines.

```text
                 PRIVATE LAB NETWORK
                 192.168.56.0/24

       ┌─────────────────────────────┐
       │       KALI LINUX            │
       │       Attacker VM           │
       │                             │
       │       192.168.56.102        │
       └──────────────┬──────────────┘
                      │
                      │ HTTP
                      │ Port 5000
                      ▼
       ┌─────────────────────────────┐
       │       UBUNTU SERVER         │
       │       Target VM             │
       │                             │
       │       192.168.56.101        │
       │                             │
       │       Flask Application     │
       │       Port 5000             │
       └─────────────────────────────┘
```

Ubuntu also had a second NAT interface:

```text
Ubuntu
├── enp0s3 → 192.168.56.101
│             Private lab network
│
└── enp0s8 → 10.0.3.15
              NAT/Internet access
```

The private interface was used for communication between Kali and Ubuntu.

---

# 6. VirtualBox Configuration

## Kali Linux

The Kali VM was configured with approximately:

| Setting   | Configuration             |
| --------- | ------------------------- |
| VM Name   | Kali-Attacker             |
| OS        | Kali Linux                |
| RAM       | 4096 MB                   |
| CPU       | 2 CPUs                    |
| Disk      | 30 GB                     |
| Disk Type | Dynamically allocated     |
| Network   | Host-only/private network |
| IP        | 192.168.56.102            |

The Kali installation was performed from:

```text
kali-linux-2026.2-installer-amd64.iso
```

A user named:

```text
rceuser
```

was created.

---

# 7. Ubuntu Target Configuration

The Ubuntu VM was configured approximately as:

| Setting  | Configuration         |
| -------- | --------------------- |
| VM Name  | Ubuntu-RCE-Target     |
| OS       | Ubuntu Server 26.04.1 |
| RAM      | 4096 MB               |
| CPU      | 2 CPUs                |
| Disk     | 25 GB                 |
| User     | rceuser               |
| Hostname | ubuntu-target         |

Ubuntu was installed from:

```text
ubuntu-26.04.1-live-server-amd64.iso
```

OpenSSH Server was also installed so that the Ubuntu machine could be accessed from Kali.

---

# 8. Network Configuration

Two network interfaces were configured on Ubuntu.

The private interface received:

```text
192.168.56.101
```

Kali received:

```text
192.168.56.102
```

Therefore:

```text
Kali
192.168.56.102
      │
      │ Private VirtualBox network
      │
Ubuntu
192.168.56.101
```

The connectivity was tested using:

```bash
ping -c 3 192.168.56.101
```

The ping test showed:

```text
3 packets transmitted
3 packets received
0% packet loss
```

This confirmed that the two virtual machines could communicate.

---

# 9. SSH Connectivity

SSH was used to manage Ubuntu from Kali.

From Kali:

```bash
ssh rceuser@192.168.56.101
```

After authentication, the Ubuntu shell was accessible.

The target identity was verified using:

```bash
whoami
```

which returned:

```text
rceuser
```

The hostname was checked using:

```bash
hostname
```

which returned:

```text
ubuntu-target
```

This confirmed that the terminal session was operating on the Ubuntu target.

---

# 10. Creating the RCE Laboratory

A dedicated project directory was created on Ubuntu:

```bash
mkdir -p ~/rce-lab
cd ~/rce-lab
```

The directory contained:

```text
app.py
venv
```

A Python virtual environment was created and used to isolate the project's Python dependencies.

The virtual environment was activated with:

```bash
. venv/bin/activate
```

The shell then displayed:

```text
(venv)
```

indicating that the virtual environment was active.

---

# 11. Flask Installation

Flask was installed inside the Python virtual environment.

The installation was verified using:

```bash
python3 -m flask --version
```

The environment showed:

```text
Python 3.14.4
Flask 3.1.3
Werkzeug 3.1.8
```

This confirmed that Flask was correctly installed.

---

# 12. Developing the Target Application

The Flask application was created in:

```text
~/rce-lab/app.py
```

The final application contained:

```python
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "RCE Lab Target Server"

@app.route("/execute")
def execute():
    cmd = request.args.get("cmd", "")

    if cmd == "hostname":
        result = subprocess.run(
            ["hostname"],
            capture_output=True,
            text=True
        )
        return f"Command executed on server: {result.stdout.strip()}"

    return "Invalid test command"

app.run(host="0.0.0.0", port=5000)
```

---

# 13. Explanation of the Application

## Flask initialization

```python
app = Flask(__name__)
```

This creates the Flask application.

---

## Root endpoint

```python
@app.route("/")
def home():
    return "RCE Lab Target Server"
```

This provides a basic endpoint to verify that the web server is running.

When Kali requested:

```text
http://192.168.56.101:5000/
```

the server returned:

```text
RCE Lab Target Server
```

---

# 14. Execution Endpoint

The application contained:

```python
@app.route("/execute")
def execute():
```

This creates an endpoint called:

```text
/execute
```

The endpoint reads the `cmd` parameter:

```python
cmd = request.args.get("cmd", "")
```

For example:

```text
/execute?cmd=hostname
```

results in:

```text
cmd = "hostname"
```

---

# 15. Controlled Execution

The application intentionally restricted execution to one harmless command:

```python
if cmd == "hostname":
```

Only when the request contains:

```text
cmd=hostname
```

does the execution code run.

The command is executed using:

```python
subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)
```

This invokes the Ubuntu operating system's `hostname` program.

The result is then returned to the requester:

```python
return f"Command executed on server: {result.stdout.strip()}"
```

This is important because the application is not simply returning:

```text
RCE successful
```

Instead, it obtains the actual hostname from the Ubuntu operating system and returns it.

---

# 16. Starting the Flask Server

The Flask application was started on Ubuntu using:

```bash
python3 app.py
```

The server reported:

```text
Running on all addresses (0.0.0.0)
```

and:

```text
http://127.0.0.1:5000
```

and:

```text
http://10.0.3.15:5000
```

Because Flask was bound to:

```text
0.0.0.0:5000
```

it listened on all IPv4 interfaces.

This was verified separately using:

```bash
ss -lntp | grep 5000
```

The result was:

```text
LISTEN 0 128 0.0.0.0:5000
```

This confirmed that the Flask service was actively listening on TCP port 5000.

---

# 17. Testing the Web Server

From Ubuntu, the service was tested locally:

```bash
curl http://192.168.56.101:5000/
```

The response was:

```text
RCE Lab Target Server
```

This confirmed that Flask was functioning correctly.

---

# 18. Testing From Kali

The same endpoint was then accessed remotely from Kali:

```bash
curl http://192.168.56.101:5000/
```

Kali received:

```text
RCE Lab Target Server
```

This established the complete network path:

```text
Kali
   ↓
192.168.56.101:5000
   ↓
Flask
   ↓
Ubuntu
```

---

# 19. RCE Demonstration

After confirming connectivity, the controlled execution endpoint was accessed from Kali.

The request was:

```bash
curl http://192.168.56.101:5000/execute?cmd=hostname
```

The response was:

```text
Command executed on server: ubuntu-target
```

---

# 20. Why This Demonstrates Server-Side Execution

The important evidence is:

```text
ubuntu-target
```

This is the hostname of the Ubuntu target.

The request originated from:

```text
Kali
192.168.56.102
```

but the operation was performed by:

```text
Ubuntu
192.168.56.101
```

The execution flow was:

```text
Kali
 │
 │ HTTP request
 │ /execute?cmd=hostname
 ▼
Ubuntu Flask
 │
 │ receives "hostname"
 ▼
subprocess.run()
 │
 ▼
Ubuntu operating system
 │
 │ hostname
 ▼
ubuntu-target
 │
 ▼
HTTP response
 │
 ▼
Kali
```

Therefore, the output was generated from the target server rather than being a predefined response.

---

# 21. Verification of the Target

The Ubuntu hostname had previously been confirmed using:

```bash
hostname
```

which returned:

```text
ubuntu-target
```

The same value was then returned through the Flask execution endpoint.

This provides a clear correlation:

```text
Direct Ubuntu command:
hostname
        ↓
ubuntu-target

Remote Flask request:
cmd=hostname
        ↓
ubuntu-target
```

This demonstrates that the Flask application caused the operation to occur on the Ubuntu server.

---

# 22. Firewall Verification

Ubuntu's firewall status was checked:

```bash
sudo ufw status
```

The result was:

```text
Status: inactive
```

Therefore, UFW was not blocking TCP port 5000.

This helped isolate the initial connectivity problem to the application/service configuration rather than the Ubuntu firewall.

---

# 23. Problems Encountered and Solutions

## Problem 1 — Flask was not reachable

Initially Kali could not connect to:

```text
192.168.56.101:5000
```

### Investigation

Network connectivity was tested using ping.

The ping succeeded:

```text
0% packet loss
```

Therefore, the basic network connection was functioning.

### Solution

The Flask service was started and verified with:

```bash
ss -lntp | grep 5000
```

which showed:

```text
0.0.0.0:5000
```

After that, Kali successfully accessed the server.

---

# 24. Problem 2 — Flask Module Not Found

At one point:

```text
ModuleNotFoundError: No module named 'flask'
```

was displayed.

### Cause

The Python virtual environment was not active.

The prompt did not contain:

```text
(venv)
```

### Solution

The environment was activated using:

```bash
. venv/bin/activate
```

Then Flask became available.

---

# 25. Problem 3 — `python` Command Not Found

Ubuntu returned:

```text
Command 'python' not found
```

### Solution

Ubuntu's available Python command was:

```bash
python3
```

Therefore the application was started using:

```bash
python3 app.py
```

---

# 26. Problem 4 — `app` Was Not Defined

An earlier version of `app.py` produced:

```text
NameError: name 'app' is not defined
```

### Cause

The Flask application initialization was missing.

### Solution

The application was corrected to include:

```python
from flask import Flask, request

app = Flask(__name__)
```

After correcting the file, Flask started normally.

---

# 27. Problem 5 — Curl Malformed URL

Kali initially produced a curl malformed URL error.

### Cause

The URL was not entered correctly.

### Solution

The request was simplified to:

```bash
curl http://192.168.56.101:5000/execute?cmd=hostname
```

The request then worked successfully.

---

# 28. Final Working Environment

At the end of the project, the environment consisted of:

### Attacker/Testing Machine

```text
Operating System: Kali Linux
IP Address: 192.168.56.102
Role: Security testing/client
```

### Target Machine

```text
Operating System: Ubuntu Server
Hostname: ubuntu-target
IP Address: 192.168.56.101
Web Server: Flask
Port: 5000
Application: app.py
```

### Network

```text
VirtualBox Host-only Network
192.168.56.0/24
```

---

# 29. Final Proof

The final successful request from Kali was:

```bash
curl http://192.168.56.101:5000/execute?cmd=hostname
```

The response was:

```text
Command executed on server: ubuntu-target
```

This demonstrated controlled server-side execution.

---

# 30. Security Significance

RCE is a serious application-security issue because unrestricted command execution can potentially allow an attacker to perform operations with the privileges of the vulnerable application.

In a real-world vulnerable application, the consequences can include:

* Unauthorized access to server resources
* Reading or modifying files
* Manipulating application data
* Running unwanted processes
* Establishing persistence
* Accessing credentials or secrets
* Further compromise of the environment

The actual impact depends on the application's privileges, operating-system permissions, network isolation, and security controls.

---

# 31. Why This Lab Was Controlled

The project was intentionally isolated using VirtualBox.

The testing environment consisted only of:

```text
Kali VM
     ↕
Ubuntu VM
```

The execution endpoint was also restricted to:

```text
hostname
```

rather than allowing arbitrary commands.

Therefore, the project demonstrates the **concept and actual server-side execution mechanism** without turning the application into an unrestricted remote shell.

---

# 32. Project Workflow

The complete workflow was:

```text
1. Install VirtualBox
        ↓
2. Install Kali Linux
        ↓
3. Install Ubuntu Server
        ↓
4. Configure private VirtualBox network
        ↓
5. Assign Kali IP
   192.168.56.102
        ↓
6. Assign Ubuntu IP
   192.168.56.101
        ↓
7. Verify ping connectivity
        ↓
8. Configure SSH access
        ↓
9. Create ~/rce-lab
        ↓
10. Create Python virtual environment
        ↓
11. Install Flask
        ↓
12. Create controlled Flask application
        ↓
13. Start Flask on port 5000
        ↓
14. Verify port 5000
        ↓
15. Test HTTP connection from Kali
        ↓
16. Send controlled execution request
        ↓
17. Ubuntu executes hostname
        ↓
18. Kali receives "ubuntu-target"
        ↓
19. RCE demonstration completed
```

---

# 33. Key Commands Used

### Create project

```bash
mkdir -p ~/rce-lab
cd ~/rce-lab
```

### Activate environment

```bash
. venv/bin/activate
```

### Check Flask

```bash
python3 -m flask --version
```

### Start application

```bash
python3 app.py
```

### Check listening port

```bash
ss -lntp | grep 5000
```

### Test server

```bash
curl http://192.168.56.101:5000/
```

### RCE proof

```bash
curl http://192.168.56.101:5000/execute?cmd=hostname
```

### Check firewall

```bash
sudo ufw status
```

### Check hostname

```bash
hostname
```

---

# 34. Evidence to Include in Your Project Presentation

For your final presentation/report, the strongest screenshots are:

### Evidence 1 — VirtualBox Architecture

Show:

```text
Kali VM
Ubuntu VM
```

### Evidence 2 — Network Configuration

Show:

```text
Kali → 192.168.56.102
Ubuntu → 192.168.56.101
```

### Evidence 3 — Successful Ping

Show Kali:

```bash
ping -c 3 192.168.56.101
```

with:

```text
0% packet loss
```

### Evidence 4 — Flask Server

Show Ubuntu:

```text
Running on 0.0.0.0:5000
```

### Evidence 5 — Port Verification

Show:

```bash
ss -lntp | grep 5000
```

with:

```text
0.0.0.0:5000
```

### Evidence 6 — HTTP Connectivity

Show Kali:

```bash
curl http://192.168.56.101:5000/
```

and:

```text
RCE Lab Target Server
```

### Evidence 7 — Actual Execution Proof

This is the most important screenshot.

Show Kali:

```bash
curl http://192.168.56.101:5000/execute?cmd=hostname
```

and:

```text
Command executed on server: ubuntu-target
```

---

# 35. Final Conclusion

The project successfully established an isolated two-machine cybersecurity laboratory using **Kali Linux and Ubuntu Server**.

A Flask web application was deployed on the Ubuntu target and exposed through port 5000. Connectivity between Kali and Ubuntu was verified using ICMP, SSH, and HTTP tests.

A controlled execution endpoint was implemented in the Flask application. From Kali, a request containing `cmd=hostname` reached the Ubuntu server. The Flask application invoked the server's `hostname` program, and the actual hostname:

```text
ubuntu-target
```

was returned to Kali.

Therefore, the project successfully demonstrated the fundamental **Remote Code Execution concept: attacker-controlled network input reaching an application and causing an operation to execute on the remote server**.

