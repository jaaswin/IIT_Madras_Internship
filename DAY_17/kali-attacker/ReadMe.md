# Kali Linux Attacker / Controller

Kali Linux is used as the attacker and controller machine in this
controlled cybersecurity laboratory.

## IP Address

Kali Linux:

192.168.56.102

## Target and Client Machines

Ubuntu Target:

192.168.56.101

Client 1:

192.168.56.103

Client 2:

192.168.56.104

## Network

All machines are connected through the isolated VirtualBox Host-only
network:

192.168.56.0/24

## Main Responsibilities

Kali Linux is used to:

1. Test connectivity with the laboratory machines.
2. Verify the Ubuntu Flask server.
3. Demonstrate the RCE vulnerability on the intentionally vulnerable
   target.
4. Verify Client 1 and Client 2.
5. Start the controlled traffic demonstration.
6. Observe the results on the Ubuntu target.

## RCE Verification

Check the target server:

curl http://192.168.56.101:5000/

RCE verification:

curl "http://192.168.56.101:5000/execute?cmd=whoami"

Hostname verification:

curl "http://192.168.56.101:5000/execute?cmd=hostname"

The returned output demonstrates that the supplied command was executed
on the Ubuntu target server.

## Client Verification

Check Client 1:

curl http://192.168.56.103:6000/

Check Client 2:

curl http://192.168.56.104:6000/

## Starting the Controlled Traffic Demonstration

Start the test on Client 1:

curl http://192.168.56.103:6000/start-test

Start the test on Client 2:

curl http://192.168.56.104:6000/start-test

The clients then generate their bounded HTTP traffic toward the Ubuntu
target.

## Monitoring

The Ubuntu target monitors incoming requests.

The target records:

- Source IP address
- Requested endpoint
- Number of requests
- Request time window

When the configured threshold is exceeded, the target generates an
alert.

Example:

[ALERT] High request rate detected from 192.168.56.103

## Attack Flow

Kali Linux
    |
    +----> Ubuntu Target
    |          |
    |          +---- RCE Demonstration
    |          |
    |          +---- Request Monitoring
    |          |
    |          +---- Alert
    |
    +----> Client 1
    |          |
    |          +---- Controlled Traffic
    |
    +----> Client 2
               |
               +---- Controlled Traffic

## Project Role

Kali Linux acts as the central testing and controller machine.

The RCE demonstration and distributed traffic demonstration are separate
parts of the project:

RCE
    |
    +--> Demonstrates initial compromise / command execution

Client 1 + Client 2
    |
    +--> Generate controlled distributed HTTP traffic

Ubuntu Target
    |
    +--> Monitors traffic and generates alerts

## Security Notice

This environment is designed for authorized cybersecurity education
and testing inside an isolated VirtualBox laboratory.

The testing should only be performed against systems that are owned
or explicitly authorized for testing.