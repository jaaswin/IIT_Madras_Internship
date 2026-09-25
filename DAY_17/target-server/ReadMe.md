# Target Server

This directory contains the Ubuntu target server used in the controlled cybersecurity laboratory.

## Components

* Flask web server
* Intentionally vulnerable RCE endpoint
* Source-IP request monitoring
* Threshold-based alerting

## Run

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
python3 app.py
```

The Flask server runs on:

```text
0.0.0.0:5000
```

## Laboratory Verification

The RCE endpoint can be verified from an authorized machine inside the isolated laboratory.

Example:

```bash
curl "http://TARGET-IP:5000/execute?cmd=whoami"
```

Another verification:

```bash
curl "http://TARGET-IP:5000/execute?cmd=hostname"
```

These commands demonstrate that the supplied command is executed on the Ubuntu target server.

## Request Monitoring

The server monitors incoming HTTP requests based on their source IP address.

The monitoring system records:

* Source IP address
* Requested endpoint
* Number of requests
* Request time window

If the configured request threshold is exceeded, an alert is displayed in the server terminal.

Example:

```text
[MONITOR] 192.168.56.103 -> / | requests in 10s: 11
[ALERT] High request rate detected from 192.168.56.103
```

## Project Purpose

The target server is used to demonstrate the relationship between:

1. RCE as an initial compromise concept
2. Multiple controlled client machines
3. Distributed HTTP traffic
4. Request monitoring
5. Abnormal traffic detection

RCE and DDoS are separate concepts in this project. RCE demonstrates command execution on the vulnerable target, while the clients are used to generate controlled distributed HTTP traffic for detection testing.

## Security Notice

This application intentionally contains a command-execution vulnerability for educational security testing.

It must only be deployed in an isolated and authorized laboratory environment.

It should **not** be exposed to the public Internet or used against systems without authorization.
