Sure 👍 Here is the \*\*complete `ReadMe.md` file\*\* ready to copy-paste.



Open it with:



```powershell

notepad ReadMe.md

```



Delete everything inside and paste this \*\*exactly as shown\*\*:



````markdown

\# Controlled DDoS Detection and Secure File Upload Lab



\## Project Overview



This project demonstrates a controlled three-machine Docker network for secure file-upload communication, abnormal traffic detection, alert generation, and traffic mitigation.



The environment contains three Docker containers:



\- \*\*Machine 1 - Legitimate Client:\*\* Uploads legitimate files to the server.

\- \*\*Machine 2 - Traffic Generator:\*\* Generates controlled excessive upload requests.

\- \*\*Machine 3 - Server + IDS:\*\* Provides the file-upload service, monitors incoming requests, detects abnormal activity, generates alerts, and applies rate limiting.



\## Architecture



```text

&#x20;                   Docker Bridge Network

&#x20;                          ddos-lab

&#x20;                              |

&#x20;            +-----------------+-----------------+

&#x20;            |                 |                 |

&#x20;            v                 v                 v

&#x20;      Machine 1          Machine 2          Machine 3

&#x20;      Legitimate         Traffic            Server + IDS

&#x20;      Client             Generator          File Upload

&#x20;            |                 |                 |

&#x20;            +-----------------+-----------------+

&#x20;                              |

&#x20;                      Request Monitoring

&#x20;                              |

&#x20;                      IDS Alert Detection

&#x20;                              |

&#x20;                        Rate Limiting

&#x20;                              |

&#x20;                    Excess Traffic Block

````



\## Machines



\### Machine 1 - Legitimate Client



Machine 1 represents a normal client.



Its responsibility is to:



\* Create a legitimate file

\* Upload the file to Machine 3

\* Verify that legitimate communication works

\* Verify that legitimate uploads continue after mitigation



Example upload command:



```bash

curl -F "file=@legitimate.txt" http://machine3-server:5000/upload

```



Expected response:



```text

{"message":"File uploaded successfully","status":"success"}

```



\---



\### Machine 2 - Traffic Generator



Machine 2 is used to generate controlled excessive upload requests against Machine 3.



This is performed only inside the private Docker lab network.



Example:



```bash

for i in {1..10}; do

&#x20; echo "Request $i"

&#x20; curl -s -o /dev/null -w "HTTP Status: %{http\_code}\\n" \\

&#x20; -F "file=@attack.txt" \\

&#x20; http://machine3-server:5000/upload

done

```



Expected result:



```text

Request 1

HTTP Status: 200



Request 2

HTTP Status: 200



Request 3

HTTP Status: 200



Request 4

HTTP Status: 200



Request 5

HTTP Status: 200



Request 6

HTTP Status: 429



Request 7

HTTP Status: 429



Request 8

HTTP Status: 429



Request 9

HTTP Status: 429



Request 10

HTTP Status: 429

```



HTTP `200` means the request was accepted.



HTTP `429` means the request was blocked because the rate limit was exceeded.



\---



\### Machine 3 - Server + IDS



Machine 3 provides the file-upload service.



It performs three main functions:



1\. File upload

2\. Request monitoring and IDS alert generation

3\. Excessive traffic mitigation using rate limiting



The server runs a Flask application on port `5000`.



The Docker host exposes the service through port `8080`.



```text

Host Port 8080

&#x20;     |

&#x20;     v

Machine 3 Container Port 5000

```



\## IDS Monitoring



The IDS monitors upload requests based on the client's IP address.



The monitoring window is:



```text

60 seconds

```



The alert threshold is:



```text

5 upload requests

```



When a client reaches the threshold, the server generates an alert.



Example:



```text

\[MONITOR] Upload request #5 from 172.18.0.3



\[ALERT] Abnormal upload activity detected

from 172.18.0.3 (5 requests in 60 seconds)

```



\## Mitigation



Flask-Limiter is used to control the number of upload requests.



The configured rate limit is:



```text

5 uploads per minute per client

```



When the client exceeds the configured limit, the server returns:



```text

HTTP 429

```



The server also generates a mitigation log:



```text

\[MITIGATION] Excessive traffic blocked

from 172.18.0.3

```



This prevents the traffic generator from continuously submitting upload requests.



\## Verification After Mitigation



After Machine 2 generates excessive traffic and the server applies rate limiting, Machine 1 can still perform a legitimate upload.



Example:



```bash

curl -s -F "file=@legitimate.txt" \\

http://machine3-server:5000/upload

```



Expected response:



```text

{"message":"File uploaded successfully","status":"success"}

```



This verifies that legitimate file-upload communication continues after the excessive traffic is mitigated.



\## Docker Network



All three machines are connected through a private Docker bridge network.



Network configuration:



```text

Network Name: ddos-lab

Driver: bridge

Subnet: 172.18.0.0/16

Gateway: 172.18.0.1

```



The containers communicate using Docker's internal DNS.



The server can therefore be accessed using:



```text

machine3-server

```



instead of using a hard-coded IP address.



Example:



```bash

http://machine3-server:5000/upload

```



\## Project Structure



```text

DAY\_13/

│

├── docker-compose.yml

│

├── server/

│   ├── app.py

│   ├── Dockerfile

│   └── requirements.txt

│

└── ReadMe.md

```



\## Technologies Used



\* Docker

\* Docker Compose

\* Python 3.12

\* Flask

\* Flask-Limiter

\* Linux

\* HTTP

\* Docker Bridge Networking



\## Requirements



Before running the project, install:



\* Docker Desktop

\* Docker Compose



Make sure Docker Desktop is running before starting the containers.



\## Running the Project



Open PowerShell and navigate to the project directory:



```powershell

cd DAY\_13

```



Build and start the containers:



```powershell

docker compose up -d --build

```



Check the running containers:



```powershell

docker ps

```



Expected containers:



```text

machine1-client

machine2-attacker

machine3-server

```



\## Access Machine 1



Run:



```powershell

docker exec -it machine1-client bash

```



Inside Machine 1:



```bash

curl http://machine3-server:5000/

```



Expected response:



```text

Machine 3 - Secure File Upload Server

```



\## Access Machine 2



Run:



```powershell

docker exec -it machine2-attacker bash

```



Inside Machine 2:



```bash

curl http://machine3-server:5000/

```



Expected response:



```text

Machine 3 - Secure File Upload Server

```



\## Monitor Machine 3



Open another PowerShell terminal and run:



```powershell

docker logs -f machine3-server

```



The server logs show:



```text

\[MONITOR]

```



for request monitoring,



```text

\[ALERT]

```



when abnormal upload activity is detected, and



```text

\[MITIGATION]

```



when excessive traffic is blocked.



\## Demonstration Flow



The complete demonstration follows this sequence:



```text

Start Docker Environment

&#x20;         |

&#x20;         v

Create Three Containers

&#x20;         |

&#x20;         v

Connect Containers to

Private Docker Network

&#x20;         |

&#x20;         v

Machine 1

Legitimate File Upload

&#x20;         |

&#x20;         v

Machine 3

Accepts File

&#x20;         |

&#x20;         v

Machine 2

Controlled Excessive Traffic

&#x20;         |

&#x20;         v

Machine 3

Monitors Requests

&#x20;         |

&#x20;         v

IDS Detects Abnormal Activity

&#x20;         |

&#x20;         v

Alert Generated

&#x20;         |

&#x20;         v

Rate Limiting Applied

&#x20;         |

&#x20;         v

Excessive Requests

Receive HTTP 429

&#x20;         |

&#x20;         v

Machine 1

Legitimate Upload Tested Again

&#x20;         |

&#x20;         v

Legitimate Upload Succeeds

```



\## Sample IDS Logs



During the demonstration, Machine 3 can produce logs similar to:



```text

\[MONITOR] Upload request #1 from 172.18.0.3

\[UPLOAD] File 'attack.txt' uploaded from 172.18.0.3



\[MONITOR] Upload request #2 from 172.18.0.3

\[UPLOAD] File 'attack.txt' uploaded from 172.18.0.3



\[MONITOR] Upload request #3 from 172.18.0.3

\[UPLOAD] File 'attack.txt' uploaded from 172.18.0.3



\[MONITOR] Upload request #4 from 172.18.0.3

\[UPLOAD] File 'attack.txt' uploaded from 172.18.0.3



\[MONITOR] Upload request #5 from 172.18.0.3

\[ALERT] Abnormal upload activity detected

from 172.18.0.3 (5 requests in 60 seconds)



\[MONITOR] Upload request #6 from 172.18.0.3

\[MITIGATION] Excessive traffic blocked from 172.18.0.3

```



\## Key Features



\### 1. Private Network



All machines communicate through a controlled Docker bridge network.



\### 2. File Upload Service



Machine 3 provides an HTTP file-upload endpoint using Flask.



\### 3. Request Monitoring



The server tracks upload requests from individual clients.



\### 4. IDS Alert



An alert is generated when abnormal upload activity reaches the configured threshold.



\### 5. Rate Limiting



Excessive requests are automatically rejected.



\### 6. Legitimate Traffic Verification



Machine 1 is tested after mitigation to verify that legitimate file uploads continue to work.



\## Learning Outcomes



This project demonstrates practical concepts including:



\* Docker containerization

\* Docker Compose

\* Docker bridge networking

\* Client-server communication

\* HTTP file uploads

\* Flask web services

\* Request monitoring

\* Intrusion Detection System concepts

\* Abnormal traffic detection

\* Alert generation

\* Rate limiting

\* Traffic mitigation

\* Network security testing



\## Security Note



This project is a controlled laboratory simulation.



The traffic generator is intended only for testing the user's own Docker-based server environment. It should not be used against systems or networks without authorization.



\## Conclusion



The project demonstrates how a server can monitor upload traffic, identify abnormal request patterns, generate IDS alerts, and mitigate excessive traffic using rate limiting.



The final verification confirms that legitimate file uploads from Machine 1 continue to function after mitigation is applied.



````



Save with \*\*Ctrl + S\*\*, then close Notepad.



\### Step 5 — Verify the first line



Run:



```powershell

type ReadMe.md

````



You should now see:



```text

\# Controlled DDoS Detection and Secure File Upload Lab

```



\*\*Do not run `git add` yet.\*\* Send me the output after you verify it, and we'll do the `.gitignore` next.



