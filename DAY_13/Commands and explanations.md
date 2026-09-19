
# DAY 13 – Project Commands

## 1. Check Docker

### Check Docker installation

```powershell
docker --version
```

**Purpose:** Checks whether Docker is installed and shows the Docker version.

---

### Check Docker Compose

```powershell
docker compose version
```

**Purpose:** Checks whether Docker Compose is installed.

---

# 2. Project Setup

### Go to the project directory

```powershell
cd C:\Users\jaasw\ddos-file-upload-lab
```

**Purpose:** Opens the folder containing your Docker project.

---

### View project files

```powershell
dir
```

**Purpose:** Shows the files and folders in the project.

Expected:

```text
docker-compose.yml
server
```

---

### View server files

```powershell
dir server
```

Expected:

```text
app.py
Dockerfile
requirements.txt
```

---

# 3. Validate the Docker Configuration

```powershell
docker compose config
```

**Purpose:** Checks whether `docker-compose.yml` is valid and displays the resolved configuration.

---

# 4. Build and Start the Lab

```powershell
docker compose up -d --build
```

**Purpose:** Builds the Machine 3 image and starts all three containers.

### Meaning:

```text
docker compose → use Docker Compose
up             → create/start containers
-d             → run in background
--build        → rebuild the image
```

---

# 5. Check Running Containers

```powershell
docker ps
```

**Purpose:** Shows the currently running containers.

You should see:

```text
machine1-client
machine2-attacker
machine3-server
```

---

# 6. Check All Containers

```powershell
docker ps -a
```

**Purpose:** Shows both running and stopped containers.

Useful for troubleshooting if a container has stopped.

---

# 7. Access Machine 1

```powershell
docker exec -it machine1-client bash
```

**Purpose:** Opens a terminal inside the legitimate client container.

You will see something similar to:

```text
root@...:/#
```

---

# 8. Access Machine 2

```powershell
docker exec -it machine2-attacker bash
```

**Purpose:** Opens a terminal inside the controlled traffic-generator container.

---

# 9. Access Machine 3

```powershell
docker exec -it machine3-server bash
```

**Purpose:** Opens a terminal inside the server container.

This is useful for checking uploaded files.

---

# 10. Exit a Container

```bash
exit
```

**Purpose:** Leaves the Docker container and returns to PowerShell.

---

# 11. Check curl

Inside Machine 1 or Machine 2:

```bash
curl --version
```

**Purpose:** Checks that `curl` is installed.

`curl` is used to send HTTP requests to the Flask server.

---

# 12. Test Server Connectivity

Inside Machine 1:

```bash
curl http://machine3-server:5000/
```

Expected:

```text
Machine 3 - Secure File Upload Server
```

### What does this prove?

It proves:

```text
Machine 1
   ↓
Docker DNS
   ↓
machine3-server
   ↓
Port 5000
   ↓
Flask Server
```

So Machine 1 can communicate with Machine 3.

---

# 13. Test From Machine 2

Inside Machine 2:

```bash
curl http://machine3-server:5000/
```

Expected:

```text
Machine 3 - Secure File Upload Server
```

**Purpose:** Confirms that Machine 2 can also communicate with Machine 3.

---

# 14. Create the Legitimate File

Inside Machine 1:

```bash
echo "This is a legitimate file from Machine 1" > legitimate.txt
```

**Purpose:** Creates the legitimate test file.

---

# 15. View the Legitimate File

```bash
cat legitimate.txt
```

Expected:

```text
This is a legitimate file from Machine 1
```

**Purpose:** Verifies the contents of the file before uploading it.

---

# 16. Upload the Legitimate File

Inside Machine 1:

```bash
curl -F "file=@legitimate.txt" http://machine3-server:5000/upload
```

**Purpose:** Uploads the legitimate file to Machine 3.

Expected:

```json
{"message":"File uploaded successfully","status":"success"}
```

### What does this prove?

It proves that the normal client can successfully use the file-upload service.

---

# 17. Check Uploaded Files

Inside Machine 3:

```bash
ls -l /app/uploads
```

**Purpose:** Displays the files stored by the server.

You should see:

```text
legitimate.txt
```

---

# 18. Read the Uploaded File

```bash
cat /app/uploads/legitimate.txt
```

**Purpose:** Confirms that the server received and stored the correct file.

---

# 19. Create the Controlled Traffic File

Inside Machine 2:

```bash
echo "Controlled traffic test from Machine 2" > attack.txt
```

**Purpose:** Creates the file used for the controlled excessive-request test.

---

# 20. View the Traffic Test File

```bash
cat attack.txt
```

**Purpose:** Verifies the file content.

---

# 21. Send One Controlled Request

```bash
curl -F "file=@attack.txt" http://machine3-server:5000/upload
```

**Purpose:** Sends one upload request from Machine 2.

Initially, the server should accept it.

---

# 22. Generate Repeated Controlled Traffic

This is the **main testing command**:

```bash
for i in {1..10}; do
  echo "Request $i"
  curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" \
  -F "file=@attack.txt" \
  http://machine3-server:5000/upload
done
```

### What does it do?

It sends 10 upload requests.

```text
Request 1
Request 2
Request 3
...
Request 10
```

The server monitors these requests.

---

# 23. Expected Result

You observed:

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

### HTTP 200

Means:

```text
Request accepted
```

### HTTP 429

Means:

```text
Too Many Requests
```

The rate limit has been exceeded.

---

# 24. Monitor Machine 3 Live

Open another PowerShell terminal:

```powershell
docker logs -f machine3-server
```

**Purpose:** Displays the Machine 3 server logs continuously.

You can observe:

```text
[MONITOR]
```

```text
[ALERT]
```

```text
[UPLOAD]
```

```text
[MITIGATION]
```

---

# 25. Stop Live Log Display

Press:

```text
Ctrl + C
```

**Purpose:** Stops following the logs.

It does **not** stop the server.

---

# 26. IDS Monitoring Log

You observed:

```text
[MONITOR] Upload request #5 from 172.18.0.2
```

**Meaning:**

The server detected the fifth upload request from that client.

The IP address may be different in another run because Docker can assign different IP addresses.

---

# 27. IDS Alert

You observed:

```text
[ALERT] Abnormal upload activity detected
from 172.18.0.2
(5 requests in 60 seconds)
```

**Meaning:**

The client reached the configured IDS threshold:

```text
5 requests
within
60 seconds
```

---

# 28. Mitigation Log

You observed:

```text
[MITIGATION] Excessive traffic blocked
from 172.18.0.2
```

**Meaning:**

The client exceeded the configured rate limit and the request was blocked.

---

# 29. Check Docker Network

From PowerShell:

```powershell
docker network inspect ddos-file-upload-lab_ddos-lab
```

**Purpose:** Displays the Docker network configuration and connected containers.

You observed:

```text
Driver: bridge
Subnet: 172.18.0.0/16
Gateway: 172.18.0.1
```

And the containers:

```text
machine1-client
machine2-attacker
machine3-server
```

---

# 30. Test the Server From Windows

From PowerShell:

```powershell
curl http://localhost:8080/
```

Expected:

```text
Machine 3 - Secure File Upload Server
```

### Why port 8080?

Docker uses:

```text
8080:5000
```

Meaning:

```text
Windows Port 8080
       ↓
Container Port 5000
       ↓
Flask Server
```

---

# 31. Final Legitimate Upload Test

After the excessive traffic has been blocked, go back to Machine 1 and run:

```bash
curl -s -F "file=@legitimate.txt" http://machine3-server:5000/upload
```

Expected:

```json
{"message":"File uploaded successfully","status":"success"}
```

### What does this prove?

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

This is one of the most important results of your project.

---

# 32. Stop the Complete Lab

When you finish the demonstration:

```powershell
docker compose down
```

**Purpose:** Stops and removes the containers and the Compose-created network.

---

# 33. Complete Demo Sequence

For your **actual project demonstration**, you mainly need these commands:

### Terminal 1 – Machine 1

```powershell
docker exec -it machine1-client bash
```

Then:

```bash
curl http://machine3-server:5000/
```

Then legitimate upload:

```bash
curl -F "file=@legitimate.txt" http://machine3-server:5000/upload
```

---

### Terminal 2 – Machine 2

```powershell
docker exec -it machine2-attacker bash
```

Then:

```bash
for i in {1..10}; do
  echo "Request $i"
  curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" \
  -F "file=@attack.txt" \
  http://machine3-server:5000/upload
done
```

---

### Terminal 3 – Machine 3 monitoring

```powershell
docker logs -f machine3-server
```

You demonstrate:

```text
MONITOR
   ↓
ALERT
   ↓
MITIGATION
   ↓
HTTP 429
```

Then return to Machine 1 and run:

```bash
curl -s -F "file=@legitimate.txt" http://machine3-server:5000/upload
```

You get:

```text
HTTP 200
```

That completes your entire demonstration:

**Legitimate Upload → Excessive Traffic → IDS Detection → Alert → Rate Limiting → HTTP 429 → Legitimate Upload Still Works.**
