


# SecureVault — Remote Code Execution (RCE) Demonstration

## Controlled Docker-Based Cybersecurity Laboratory

> **Purpose:** Academic and authorized cybersecurity research and demonstration  
> **Project:** SecureVault  
> **Focus:** Unrestricted File Upload → PHP Execution → Controlled Remote Code Execution  
> **Environment:** Docker, Apache, PHP 8.2, cURL  
> **Author:** Shad

---

## 1. Project Overview

SecureVault is a deliberately vulnerable PHP web application created to study how an insecure file-upload implementation can lead to **Remote Code Execution (RCE)**.

The objective of this project was not simply to upload a file. The purpose was to understand the complete security chain:

```text
Attacker
   |
   | HTTP request
   v
Upload API
   |
   | PHP file accepted
   v
Web-accessible upload directory
   |
   | Request uploaded .php file
   v
Apache
   |
   v
PHP Interpreter
   |
   v
PHP Code Execution
   |
   v
Controlled OS Command Execution
   |
   v
HTTP Response
````

The laboratory was intentionally designed with several insecure conditions:

* The upload API did not require authentication.
* The upload API did not enforce an extension allowlist.
* PHP files could be uploaded.
* Uploaded files were stored inside the Apache document root.
* PHP execution was enabled for files in that location.
* The RCE proof deliberately passed HTTP input to PHP's `system()` function.

These weaknesses were combined only inside an isolated Docker laboratory.

The documented project establishes that an uploaded PHP file was actually interpreted by PHP and that controlled operating-system commands could execute in the web-server process context. The documented execution identity was `www-data`. 

---

# 2. Problem Statement

File-upload functionality is a common feature in web applications.

Examples include:

* profile-picture uploads,
* document uploads,
* medical documents,
* invoices,
* reports,
* images,
* and attachments.

A secure upload implementation must answer four important questions:

1. **Who is allowed to upload?**
2. **What type of file can be uploaded?**
3. **Where should the file be stored?**
4. **Can the uploaded file ever be executed as server-side code?**

The SecureVault laboratory intentionally removes several of these protections.

The main security question investigated was:

> Can an unauthenticated user upload a PHP file, access that file through Apache, cause PHP to interpret it, and demonstrate server-side command execution?

The documented answer was yes within the controlled laboratory. The upload API accepted PHP, stored it under `/var/www/html/uploads`, and Apache/PHP interpreted the uploaded file.

---

# 3. Why I Created This Project

I created this project to understand the difference between:

```text
File Upload
```

and

```text
Executable File Upload
```

A normal file-upload vulnerability may allow an attacker to place an unwanted file on a server.

The impact becomes substantially more serious when:

```text
Uploaded file
      +
Executable extension
      +
Web-accessible location
      +
Server-side interpreter
```

are combined.

The project therefore focuses on understanding the complete vulnerability chain instead of looking at file upload as an isolated feature.

The project also helped demonstrate the difference between:

* application-level RCE,
* Docker administrative access,
* server-process privileges,
* and an interactive shell.

The laboratory documentation specifically distinguishes RCE from direct Docker administration and from a persistent interactive shell.

---

# 4. Project Objectives

The main objectives were:

* Build a reproducible Docker security laboratory.
* Run PHP 8.2 with Apache.
* Create a custom web application called SecureVault.
* Implement a file-upload API.
* Demonstrate unauthenticated file upload.
* Test whether PHP files could be uploaded.
* Verify that uploaded PHP files were interpreted by Apache/PHP.
* Demonstrate controlled server-side command execution.
* Identify the execution user.
* Demonstrate controlled application-file access.
* Analyze the root causes of the vulnerability.
* Understand the complete upload-to-RCE attack chain.
* Explain the security impact.
* Design a secure upload architecture.
* Document the complete process for academic evaluation.

---

# 5. Laboratory Scope

This project was performed as a controlled Docker laboratory.

The environment contains separate containers for:

* the vulnerable SecureVault server,
* a normal client,
* and a controlled attacker/security-testing container.

The containers communicate through a private Docker bridge network.

The laboratory does not target external systems.

The RCE demonstration uses controlled information commands such as:

```text
whoami
hostname
pwd
uname -a
ls -la
```

The objective is to prove server-side execution without requiring destructive activity.

---

# 6. Architecture

The SecureVault architecture is:

```text
                         Private Docker Network
                  rce-file-upload-lab_rce-lab-network

             +-----------------------------+
             |                             |
             |       Attacker Container    |
             |       curl / testing        |
             |                             |
             +-------------+---------------+
                           |
                           | HTTP
                           |
                           v
             +-----------------------------+
             |                             |
             |       Server Container      |
             |                             |
             |       Apache                |
             |       PHP 8.2               |
             |       SecureVault           |
             |                             |
             |       /var/www/html         |
             |       /uploads               |
             |                             |
             +-------------+---------------+
                           ^
                           |
                           | HTTP
                           |
             +-------------+---------------+
             |                             |
             |       Client Container      |
             |       Normal testing        |
             |                             |
             +-----------------------------+

Host:
localhost:8081  --->  server:80
```

The project documentation identifies the Docker services as:

| Service    | Purpose                                  |
| ---------- | ---------------------------------------- |
| `server`   | PHP 8.2 + Apache SecureVault application |
| `client`   | Normal application/client testing        |
| `attacker` | Controlled security-testing container    |

The server was exposed through:

```text
localhost:8081 → container port 80
```

The attacker communicates with the server internally using the Docker service name.

---

# 7. Technologies Used

## Docker

Docker was used to create isolated and reproducible laboratory machines.

## Docker Compose

Docker Compose was used to define the server, client and attacker services.

## Apache

Apache was used as the web server.

## PHP 8.2

PHP was used as the server-side programming language and interpreter.

## cURL

cURL was used to perform controlled HTTP requests from the attacker container.

## Linux

The SecureVault server runs in the Linux-based PHP/Apache Docker environment.



# 8. Project Structure

The main project directory was:

```text
C:\Users\jaasw\rce-file-upload-lab
```

Important files include:

```text
rce-file-upload-lab/
│
├── docker-compose.yml
│
├── server/
│   ├── Dockerfile
│   ├── index.php
│   ├── login.php
│   ├── dashboard.php
│   ├── upload.php
│   ├── status.php
│   │
│   ├── api/
│   │   └── upload.php
│   │
│   ├── uploads/
│   └── previews/
│
├── client/
│
├── attacker/
│
└── proof.php
```

The Stage 3 documentation identifies these files as the important components of the laboratory. 

---

# 9. Server Configuration

The server image was based on:

```dockerfile
FROM php:8.2-apache
```

The Apache document root was:

```text
/var/www/html
```

The upload directory was:

```text
/var/www/html/uploads
```

The server also created:

```text
/var/www/html/previews
```

The upload and preview directories were assigned to:

```text
www-data:www-data
```

The important configuration was:

```text
Apache document root
        |
        v
/var/www/html
        |
        +-- index.php
        +-- login.php
        +-- dashboard.php
        +-- upload.php
        +-- api/
        |
        +-- uploads/
        |
        +-- previews/
```

The critical design problem is that `uploads/` exists **inside** the Apache document root.

---

# 10. Normal SecureVault Application Flow

SecureVault contains a normal application/login flow.

The application includes:

```text
index.php
login.php
dashboard.php
upload.php
status.php
```

The login flow establishes a session and allows the user to reach the dashboard.

However, the vulnerable API was implemented separately:

```text
/api/upload.php
```

This distinction became important during the security analysis.

The normal application had a login concept, but the vulnerable upload API did not enforce the same authentication/authorization check.

Therefore:

```text
Normal Dashboard
       |
       v
Authentication required

Vulnerable API
       |
       v
Authentication not enforced
```

The documented demo credentials were only laboratory credentials. The actual security finding was that the vulnerable upload endpoint itself did not require the dashboard session. 

---

# 11. Vulnerable Upload API

The vulnerable endpoint was:

```text
/api/upload.php
```

The important implementation characteristics were:

```text
POST request
    |
    v
Receive uploaded file
    |
    v
No authentication check
    |
    v
No extension allowlist
    |
    v
Generate filename
    |
    v
Save into /var/www/html/uploads/
```

The intentionally vulnerable design was documented as:

```php
/*
 * INTENTIONAL LAB VULNERABILITY:
 * - No authentication/authorization check
 * - No file-extension allowlist
 * - Uploaded files are stored inside the web root
 */
```

This design was deliberately created to demonstrate the vulnerability chain. 

---

# 12. Why Authentication Was Important

The normal SecureVault application contained authentication.

However, the vulnerable upload API did not enforce authentication.

This means an attacker could interact with the upload functionality without first going through the application's normal login process.

The security problem can therefore be represented as:

```text
Expected:

User
 ↓
Login
 ↓
Authentication
 ↓
Authorization
 ↓
Upload


Vulnerable implementation:

User
 ↓
Upload API
 ↓
File accepted
```

The missing authorization check increased the attack surface.

---

# 13. Why the Extension Allowlist Was Important

A secure application should normally define which file types it actually needs.

For example:

```text
.jpg
.jpeg
.png
.pdf
```

The vulnerable application did not restrict the extension.

Therefore:

```text
test.txt
```

and

```text
proof.php
```

could both be submitted to the same upload API.

The problem is particularly serious because PHP was an executable server-side file type.

---

# 14. Why Web-Root Storage Was Dangerous

The application stored files under:

```text
/var/www/html/uploads/
```

But:

```text
/var/www/html
```

was Apache's document root.

Therefore:

```text
/var/www/html/uploads/file.php
```

was accessible through HTTP as:

```text
/uploads/file.php
```

This created the critical relationship:

```text
File Storage
     |
     v
Web Root
     |
     v
HTTP Accessible
     |
     v
PHP Enabled
     |
     v
Executable
```

The Stage 3 documentation specifically identifies this web-root placement as a root cause.

---

# 15. Why `uniqid()` Did Not Fix the Vulnerability

The application generated a new filename using `uniqid()`.

For example:

```text
api_upload_<random-value>.php
```

This makes filenames harder to predict.

However, it does **not** make the file safe.

If the generated filename still ends in:

```text
.php
```

and is stored inside the PHP-enabled web root, Apache/PHP can still interpret it.

Therefore:

```text
Random filename
       ≠
Safe file
```

The important security property is the file's type, location and execution behavior.

---

# 16. Stage 3 Implementation Process

The implementation followed a controlled sequence.

### Step 1 — Create Docker laboratory

I created the Docker Compose environment containing:

```text
server
client
attacker
```

### Step 2 — Build PHP/Apache server

The server was based on:

```text
php:8.2-apache
```

### Step 3 — Configure SecureVault

The application files were copied into:

```text
/var/www/html
```

### Step 4 — Create upload directory

The vulnerable directory was:

```text
/var/www/html/uploads
```

### Step 5 — Create vulnerable upload API

The API accepted uploaded files without the necessary security restrictions.

### Step 6 — Start the containers

The environment was started using Docker Compose.

### Step 7 — Verify the server

The PHP version and Apache configuration were checked.

### Step 8 — Test normal file upload

A harmless text file was uploaded.

### Step 9 — Test PHP execution

A controlled PHP proof was uploaded.

### Step 10 — Demonstrate RCE

A separate controlled proof used PHP `system()` with a command parameter.

### Step 11 — Verify execution context

`whoami` showed:

```text
www-data
```

### Step 12 — Analyze impact

A laboratory-only application secret was used to demonstrate controlled file access.

### Step 13 — Design mitigation

The insecure upload architecture was redesigned conceptually.

The documented implementation sequence follows this progression. 

---

# 17. Initial Server Verification

After starting the environment, the containers were checked.

```bash
docker compose ps
```

The expected services were:

```text
server
client
attacker
```

The server was mapped to:

```text
localhost:8081
```

---

# 18. PHP Version Verification

The PHP version was checked using:

```bash
docker compose exec server sh -c "php -v"
```

The documented result was:

```text
PHP 8.2.34
```

This confirmed that the expected PHP environment was running. 

---

# 19. Apache Verification

Apache configuration was inspected using:

```bash
docker compose exec server sh -c "apache2ctl -S"
```

The important result was that the Apache document root was:

```text
/var/www/html
```

This was critical to the experiment because the upload directory was underneath this path.



---

# 20. First Test — PHP Execution in Uploads

Before demonstrating RCE, I first proved something simpler:

> Can Apache/PHP execute a PHP file placed inside the upload directory?

A simple PHP file was used:

```php
<?php
echo "SECUREVAULT_UNAUTHENTICATED_PHP_EXECUTION_PROOF";
?>
```

The file was placed in the upload directory through the vulnerable upload functionality.

It was then requested through HTTP.

The documented test showed PHP-generated output and:

```text
X-Powered-By: PHP/8.2.34
```

This proved that uploaded PHP files were being interpreted by Apache/PHP.



---

# 21. Why the PHP Execution Test Was Necessary

It would not be sufficient to simply say:

> "The application allows PHP upload, therefore RCE exists."

The test was divided into separate stages.

### Stage A

Prove that file upload works.

### Stage B

Prove that a PHP file can be uploaded.

### Stage C

Prove that the uploaded PHP file is interpreted.

### Stage D

Prove that the PHP file can execute a controlled OS command.

This makes the security demonstration much stronger because each stage establishes one part of the chain.

---

# 22. Second Test — Unauthenticated Upload

A harmless text file was used first.

Example:

```bash
printf '%s\n' 'CONTROLLED_UPLOAD_TEST_2' > /tmp/test.txt
```

Then it was uploaded through:

```text
/api/upload.php
```

The documented API response was similar to:

```json
{
  "status": "success",
  "original_name": "test.txt",
  "stored_name": "api_upload_<generated>.txt"
}
```

This proved that the endpoint accepted an upload without requiring the normal dashboard session.



---

# 23. Generated Filenames

The server generated filenames such as:

```text
api_upload_<unique-value>.txt
```

For PHP files, the generated name ended with:

```text
.php
```

Because every upload receives a new generated name, the current `stored_name` from the API response must be used when performing a later test.

An old generated filename may return:

```text
404 Not Found
```

This was an important troubleshooting point during the implementation.

---

# 24. RCE Proof

After PHP execution had been established, I created a controlled RCE proof.

The proof was:

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

This code is intentionally vulnerable and exists only for the laboratory demonstration.

---

# 25. How the RCE Proof Works

The execution chain is:

```text
HTTP Request
     |
     v
$_GET['cmd']
     |
     v
PHP system()
     |
     v
Linux command
     |
     v
Command output
     |
     v
HTTP response
```

For example, the conceptual request:

```text
/uploads/<stored-name>.php?cmd=whoami
```

causes:

```text
$_GET['cmd']
       |
       v
"whoami"
       |
       v
system("whoami")
```

The result is returned through the HTTP response.

This establishes remote server-side command execution.

The project documentation explicitly identifies this as the final RCE proof.

---

# 26. Harmless Verification Commands

The RCE proof was tested with information-gathering commands.

| Command               | Purpose                               |
| --------------------- | ------------------------------------- |
| `whoami`              | Determine execution identity          |
| `hostname`            | Identify target container             |
| `pwd`                 | Identify working directory            |
| `uname -a`            | Display system information            |
| `ls -la`              | Display accessible directory contents |
| `ps`                  | Display visible processes             |
| `df -h`               | Display filesystem information        |
| `free -h`             | Display memory information            |
| `cat /etc/os-release` | Identify operating-system information |

These commands were used to demonstrate execution without requiring destructive actions. 

---

# 27. Execution Identity

The most important RCE verification command was:

```text
whoami
```

The documented result was:

```text
www-data
```

This means the command was executed within the web-server process context.

It does **not** mean that the attacker automatically obtained root privileges.

The effective permissions depend on the account running the application and the permissions assigned to that account.

---

# 28. Why `www-data` Is Important

The execution identity demonstrates the security boundary.

The architecture is:

```text
HTTP Request
      |
      v
Apache
      |
      v
PHP
      |
      v
system()
      |
      v
www-data
      |
      v
Operating System
```

Therefore the demonstrated RCE executes with the privileges available to the web application.

This is an important security lesson:

> RCE describes the ability to execute remotely; it does not automatically describe the privilege level of that execution.

---

# 29. Controlled Secret Demonstration

To demonstrate application-level impact safely, a laboratory-only file was created:

```text
/var/www/html/lab-secret.txt
```

It contained a lab-only value:

```text
SECUREVAULT_WEBAPP_SECRET=LAB-ONLY-ACCESS-9281
```

A controlled PHP proof used `file_get_contents()` to read the file.

The purpose was to demonstrate that executed PHP could access application-readable data.

This demonstrated:

* PHP file operations,
* access based on filesystem permissions,
* application-level impact,
* and the fact that RCE does not require root access.

The secret was intentionally laboratory-only and should not be treated as a real credential.

---

# 30. What the Secret Demonstration Does Not Prove

The controlled secret demonstration does **not** prove:

* root access,
* host-machine compromise,
* Docker escape,
* access to production credentials,
* access to external systems,
* or persistence.

It only demonstrates that code executing in the web-process context can access files permitted to that process.

---

# 31. Docker Shell vs RCE

This distinction is extremely important.

## Docker administrative shell

```bash
docker compose exec server sh
```

This means the operator already has Docker access.

It directly enters the container.

## Application RCE

The RCE path is:

```text
Attacker
   |
   | HTTP
   v
Apache
   |
   v
PHP
   |
   v
Uploaded PHP
   |
   v
system()
   |
   v
Operating system
```

The second path demonstrates the actual application vulnerability.

The documentation specifically distinguishes direct Docker administration from application-level RCE. 

---

# 32. RCE Does Not Require an Interactive Shell

An important concept learned during the project is that RCE does not require a persistent interactive shell.

The HTTP proof is sufficient:

```text
HTTP Request
     ↓
Server executes command
     ↓
HTTP Response
```

This is request/response-based RCE.

A persistent interactive network shell would be a separate technique and is not required to establish the vulnerability.

The documented project explicitly makes this distinction.

---

# 33. Complete Attack Chain

The complete SecureVault chain is:

```text
1. Attacker reaches upload API
              |
              v
2. Authentication is not enforced
              |
              v
3. Attacker uploads PHP file
              |
              v
4. Server stores PHP under web root
              |
              v
5. Apache exposes uploaded file
              |
              v
6. PHP interprets uploaded source
              |
              v
7. PHP receives controlled HTTP input
              |
              v
8. system() executes command
              |
              v
9. Command executes as www-data
              |
              v
10. Output is returned through HTTP
```

This is the central finding of Stage 3.

---

# 34. Root Cause Analysis

## Root Cause 1 — Missing Authentication

The upload API did not enforce authentication.

### Impact

An unauthenticated request could reach the upload functionality.

---

## Root Cause 2 — Missing Authorization

Even if authentication existed elsewhere in the application, the API did not enforce the required authorization decision.

### Impact

The upload operation was not protected by the application's normal access-control model.

---

## Root Cause 3 — No Extension Allowlist

The API did not prevent PHP extensions.

### Impact

Executable server-side content could be submitted.

---

## Root Cause 4 — Web-Root Storage

Uploaded files were stored under:

```text
/var/www/html/uploads
```

### Impact

Uploaded files were directly reachable through HTTP.

---

## Root Cause 5 — PHP Execution Enabled

Apache/PHP interpreted `.php` files in the upload directory.

### Impact

The uploaded object became executable code instead of remaining data.

---

## Root Cause 6 — Excessive Trust in Uploaded Content

The application treated uploaded content as safe enough to store and serve without separating data from executable code.

### Impact

Attacker-controlled content crossed the application/code boundary.

---

# 35. Security Impact

The demonstrated vulnerability can potentially allow an attacker to move from:

```text
File Upload
```

to:

```text
Server-Side Code Execution
```

The actual impact depends on:

* the web-process privileges,
* filesystem permissions,
* application permissions,
* container isolation,
* accessible configuration,
* network connectivity,
* and other security controls.

In the laboratory, the observed execution identity was:

```text
www-data
```

Therefore the demonstrated impact is specifically execution within the web-process context.

---

# 36. Secure Mitigation

The vulnerable architecture should be replaced with a defense-in-depth design.

```text
Authenticated User
        |
        v
Authorization Check
        |
        v
Extension Allowlist
        |
        v
Content Validation
        |
        v
Safe Filename
        |
        v
Storage Outside Web Root
        |
        v
Script Execution Disabled
        |
        v
Least-Privilege Permissions
        |
        v
Monitoring and Logging
```

---

# 37. Mitigation 1 — Authentication

The upload endpoint should require an authenticated user.

Example concept:

```text
Request
  |
  v
Authenticated?
  |
  +-- No --> Reject
  |
  +-- Yes
        |
        v
Continue
```

This prevents anonymous users from directly reaching sensitive functionality.

---

# 38. Mitigation 2 — Authorization

Authentication alone is not sufficient.

The application should verify that the authenticated user has permission to upload.

For example:

```text
Authenticated
     |
     v
Authorized for upload?
     |
     +-- No --> Reject
     |
     +-- Yes --> Continue
```

---

# 39. Mitigation 3 — Extension Allowlist

The application should explicitly define allowed file types.

For example:

```text
Allowed:

.jpg
.jpeg
.png
.pdf
```

Everything else should be rejected unless there is a genuine business requirement.

Executable extensions such as:

```text
.php
```

should not be accepted when PHP uploads are not required.

---

# 40. Mitigation 4 — Content Validation

Checking only the filename is insufficient.

The application should validate:

* MIME type,
* file structure,
* file size,
* expected content,
* and, where appropriate, image dimensions.

The purpose is to ensure that the uploaded object actually matches the expected file type.

---

# 41. Mitigation 5 — Store Outside the Web Root

The vulnerable design uses:

```text
/var/www/html/uploads
```

A secure design should instead use a directory that Apache cannot directly execute.

For example:

```text
/var/lib/securevault/uploads
```

The application can then provide controlled download functionality.

This separates:

```text
User-controlled data
```

from:

```text
Executable application code
```

---

# 42. Mitigation 6 — Disable Script Execution

The upload directory should not execute PHP.

Even if an unexpected file reaches the directory:

```text
file.php
```

it should be treated as data and not executed by Apache.

This provides an additional layer of protection.

---

# 43. Mitigation 7 — Least Privilege

The web application should have only the permissions it requires.

The web process should not unnecessarily access:

* operating-system secrets,
* private keys,
* administrative files,
* unrelated applications,
* sensitive configuration,
* or user data outside its intended scope.

---

# 44. Mitigation 8 — Monitoring and Logging

The application should log security-relevant events.

Examples include:

```text
Upload attempted
Upload rejected
Unexpected extension
Invalid MIME type
Large upload
Repeated upload attempts
Authentication failure
Suspicious request
```

These logs can help identify abuse and support incident investigation.

---

# 45. Secure Architecture

The final recommended architecture is:

```text
                  SecureVault

                       |
                       v
              +----------------+
              | Authentication |
              +-------+--------+
                      |
                      v
              +----------------+
              | Authorization  |
              +-------+--------+
                      |
                      v
              +----------------+
              | File Validation|
              +-------+--------+
                      |
                      v
              +----------------+
              | Allowlist      |
              +-------+--------+
                      |
                      v
              +----------------+
              | Safe Filename  |
              +-------+--------+
                      |
                      v
              +----------------------+
              | Storage Outside      |
              | Web Document Root    |
              +----------+-----------+
                         |
                         v
              +----------------------+
              | Script Execution     |
              | Disabled             |
              +----------+-----------+
                         |
                         v
              +----------------------+
              | Least Privilege      |
              +----------+-----------+
                         |
                         v
              +----------------------+
              | Monitoring / Logging |
              +----------------------+
```

---

# 46. Testing Methodology

The testing was performed progressively.

## Test 1 — Service availability

Verify:

```bash
docker compose ps
```

## Test 2 — PHP environment

Verify:

```bash
docker compose exec server sh -c "php -v"
```

Expected:

```text
PHP 8.2.34
```

## Test 3 — Apache configuration

Verify:

```bash
docker compose exec server sh -c "apache2ctl -S"
```

Expected document root:

```text
/var/www/html
```

## Test 4 — Upload directory

Verify:

```bash
docker compose exec server sh -c "ls -la /var/www/html/uploads"
```

## Test 5 — Harmless upload

Upload a text file.

## Test 6 — PHP execution

Upload the controlled PHP proof and request it.

## Test 7 — RCE

Use harmless information commands.

## Test 8 — Execution identity

Verify:

```text
whoami → www-data
```

## Test 9 — Controlled application file access

Read the laboratory-only secret.

## Test 10 — Mitigation analysis

Verify that the secure design prevents executable uploads from becoming server-side code.

---

# 47. Troubleshooting

## Problem: `Method not allowed`

If:

```text
http://localhost:8081/api/upload.php
```

is opened directly in a browser, the browser sends a GET request.

The API expects POST.

Therefore:

```text
405 Method Not Allowed
```

is expected.

---

## Problem: 404 after uploading PHP

The upload API generates a new filename every time.

Therefore an old filename may no longer exist.

Always use:

```text
stored_name
```

from the latest upload response.

---

## Problem: PHP does not execute

Verify:

```bash
docker compose exec server sh -c "php -v"
```

Then verify Apache:

```bash
docker compose exec server sh -c "apache2ctl -S"
```

Then verify the file location:

```text
/var/www/html/uploads/
```

---

## Problem: Attacker cannot reach server

Verify containers:

```bash
docker compose ps
```

Then test the Docker service name:

```text
server
```

Docker's internal DNS allows the attacker container to resolve the service.

---

# 48. Evidence Checklist

| Evidence               | Expected result                      |
| ---------------------- | ------------------------------------ |
| Docker services        | server, client and attacker running  |
| Host mapping           | `localhost:8081 → server:80`         |
| PHP                    | PHP 8.2.34                           |
| Apache                 | `/var/www/html` document root        |
| Upload directory       | `/var/www/html/uploads`              |
| Unauthenticated upload | Success JSON                         |
| PHP execution          | PHP-generated output                 |
| RCE                    | Command output returned              |
| `whoami`               | `www-data`                           |
| Lab secret             | Controlled application data readable |
| Secure design          | Executable uploads prevented         |

The source report provides the same evidence checklist and expected results. 

---

# 49. Presentation Procedure

For a project demonstration, the recommended sequence is:

### 1. Introduce SecureVault

Explain that it is an isolated Docker-based vulnerable web application.

### 2. Show Docker containers

```bash
docker compose ps
```

Identify:

```text
server
client
attacker
```

### 3. Explain the private network

Explain that the attacker communicates with the server through the Docker network.

### 4. Show normal application

Demonstrate the login/dashboard context.

### 5. Show vulnerable API

Open:

```text
server/api/upload.php
```

Explain:

* no authentication,
* no extension allowlist,
* web-root storage.

### 6. Upload harmless file

Demonstrate that the API accepts a file.

### 7. Upload PHP proof

Show that PHP executes from the upload directory.

### 8. Demonstrate RCE

Use harmless commands such as:

```text
whoami
hostname
pwd
```

### 9. Explain `www-data`

Explain that the command executes under the web-process account.

### 10. Explain Docker vs RCE

Show why:

```text
docker compose exec
```

is not the vulnerability.

### 11. Show controlled impact

Optionally demonstrate the lab-only application secret.

### 12. Finish with mitigation

Show:

```text
Authentication
      ↓
Authorization
      ↓
Validation
      ↓
Allowlist
      ↓
Non-web-root storage
      ↓
No script execution
      ↓
Least privilege
      ↓
Monitoring
```

This presentation sequence follows the documented Stage 3 procedure. 

---

# 50. Viva Questions and Answers

### What is RCE?

Remote Code Execution is the ability to cause code or commands to execute remotely on a target system.

### Why is SecureVault vulnerable?

Because the upload API allows unauthenticated uploads, does not restrict executable file types, stores uploads in the web root, and allows PHP execution.

### Why does PHP execute inside `uploads`?

Because the directory is under Apache's document root and PHP execution is enabled.

### Why does `whoami` return `www-data`?

Because Apache/PHP processes the request under the web-server service account.

### Does RCE mean root access?

No.

RCE describes remote execution. The privileges depend on the process account.

### Why is `docker compose exec server sh` not RCE?

Because it is direct Docker administrative access and bypasses the application vulnerability.

### Why did authentication not protect the upload?

Because the vulnerable API did not enforce the application's normal session/authentication check.

### Why does the uploaded filename change?

The API uses `uniqid()` to generate a new stored filename.

### How should SecureVault be fixed?

Use authentication, authorization, strict allowlisting, content validation, non-web-root storage, disabled script execution and least privilege.

### Is an interactive shell required to prove RCE?

No.

The documented HTTP request/response command execution is sufficient to demonstrate RCE. 

---

# 51. What I Learned From This Project

This project provided practical understanding of:

* Docker containerization.
* Docker networking.
* Apache configuration.
* PHP execution.
* HTTP file uploads.
* Authentication and authorization.
* File validation.
* Web-root security.
* Server-side code execution.
* RCE.
* Linux process identities.
* `www-data`.
* Filesystem permissions.
* Security testing methodology.
* Vulnerability root-cause analysis.
* Defense in depth.
* Secure architecture design.
* Security documentation.

---

# 52. Main Security Lesson

The most important lesson from SecureVault is:

```text
Untrusted File
     +
Executable Extension
     +
Web-Accessible Location
     +
Server-Side Interpreter
     =
Potential RCE
```

Removing any one of these dangerous conditions can reduce the attack path.

A secure application should therefore ensure that:

```text
User Upload
     ↓
Validated Data
     ↓
Non-Executable Storage
```

rather than:

```text
User Upload
     ↓
Web Root
     ↓
Executable PHP
     ↓
Server Code Execution
```

---

# 53. Final Conclusion

The SecureVault laboratory successfully demonstrated a complete chain from **unauthenticated file upload to PHP execution and controlled operating-system command execution**.

The key problem was not one individual line of code. It was the combination of several insecure design decisions:

```text
Missing Authentication
        +
Missing Authorization
        +
No Extension Allowlist
        +
Web-Root Storage
        +
PHP Execution
        =
Upload-Driven RCE
```

The first PHP execution proof established that the uploaded file was actually interpreted by Apache/PHP.

The second proof established controlled operating-system command execution through:

```text
HTTP
 ↓
$_GET['cmd']
 ↓
system()
 ↓
OS command
 ↓
HTTP response
```

The `whoami` result:

```text
www-data
```

confirmed that execution occurred within the web-server process context.

The project also demonstrated that:

```text
RCE ≠ Root Access
```

and:

```text
Docker Administrative Shell ≠ Application RCE
```

The correct production solution is not simply to rename uploaded files. The application must prevent user-controlled content from becoming executable server-side code.

The secure design should therefore use:

```text
Authentication
       ↓
Authorization
       ↓
Strict Allowlist
       ↓
Content Validation
       ↓
Safe Filename
       ↓
Storage Outside Web Root
       ↓
Script Execution Disabled
       ↓
Least Privilege
       ↓
Monitoring and Logging
```

This project demonstrates the complete security lifecycle:

```text
Build
  ↓
Test
  ↓
Observe
  ↓
Verify
  ↓
Analyze
  ↓
Identify Root Cause
  ↓
Mitigate
  ↓
Design Secure Architecture
  ↓
Document
```

---

# 54. Project Safety Statement

This repository contains cybersecurity laboratory material intended for:

* academic demonstrations,
* authorized security testing,
* controlled Docker environments,
* and security education.

The SecureVault application is intentionally vulnerable.

The RCE proof is included to demonstrate the vulnerability inside the controlled laboratory.

The techniques documented here should only be used against systems for which explicit authorization has been obtained.

Do not deploy the intentionally vulnerable SecureVault configuration in a production environment.

---

# 55. Repository Structure

A recommended GitHub structure is:

```text
securevault-security-lab/
│
├── README.md
│
├── server/
│   ├── Dockerfile
│   ├── index.php
│   ├── login.php
│   ├── dashboard.php
│   ├── upload.php
│   ├── status.php
│   │
│   └── api/
│       └── upload.php
│
├── client/
│
├── attacker/
│
├── screenshots/
│   ├── docker-containers.png
│   ├── securevault-login.png
│   ├── upload-api.png
│   ├── php-execution.png
│   ├── rce-proof.png
│   └── mitigation.png
│
├── docs/
│   └── SecureVault-Stage3-Report.pdf
│
├── docker-compose.yml
├── proof.php
├── .gitignore
└── LICENSE
```

---

# SecureVault Stage 3 — Final Project Statement

**SecureVault demonstrates how an insecure file-upload design can result in Remote Code Execution. I created an isolated Docker environment containing Apache, PHP 8.2, a vulnerable SecureVault application, a normal client and a controlled attacker container. I intentionally created an upload API without authentication/authorization enforcement, without a PHP extension restriction, and with uploads stored inside the Apache document root. I first verified normal file upload, then verified that an uploaded PHP file was interpreted by Apache/PHP. Finally, I used a controlled PHP RCE proof to demonstrate server-side command execution and verified that execution occurred as `www-data`. I then analyzed the root causes and designed a secure architecture using authorization, strict validation, non-web-root storage, disabled script execution and least privilege.**

```

The technical details above are grounded in your supplied SecureVault Stage 3 report, including its architecture, implementation sequence, verification results, RCE proof, `www-data` execution context, controlled-secret demonstration, troubleshooting, mitigation and presentation procedure. 
```
