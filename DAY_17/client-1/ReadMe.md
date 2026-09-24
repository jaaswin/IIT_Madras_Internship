# Client 1

Client 1 is a controlled traffic-generating machine in the cybersecurity
laboratory.

## Purpose

Client 1 is used to:

- Communicate with the Ubuntu target server
- Generate bounded HTTP requests
- Demonstrate distributed traffic
- Test the target server's request monitoring and alert mechanism

## Configuration

Client 1 IP:

192.168.56.103

Target server:

192.168.56.101:5000

Agent port:

6000

## Installation

Create a virtual environment:

python3 -m venv venv

Activate it:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Start Client 1

Run:

python3 lab-agent.py

The client agent listens on:

0.0.0.0:6000

## Start Controlled Traffic

From the authorized Kali controller:

curl http://192.168.56.103:6000/start-test

The client generates a bounded number of HTTP requests toward the
Ubuntu target.

## Traffic Test

The traffic-test.py script sends 20 HTTP requests with a short delay
between requests.

The target server records the requests and can generate an alert when
the configured request-rate threshold is exceeded.

## Project Role

Client 1 represents one participating host in the controlled distributed
traffic demonstration.

The project uses multiple independent clients to demonstrate how traffic
from different source IP addresses can be observed by the target.

## Security Notice

This client is intended only for an isolated and authorized cybersecurity
laboratory.

The traffic generation is deliberately bounded and should not be used
against systems without authorization.