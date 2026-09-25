from flask import Flask, request
import subprocess
import time

app = Flask(__name__)

# Request monitoring
request_log = {}
ALERT_THRESHOLD = 10
WINDOW = 10


@app.before_request
def monitor_request():
    ip = request.remote_addr
    now = time.time()

    if ip not in request_log:
        request_log[ip] = []

    # Keep only requests from the last WINDOW seconds
    request_log[ip] = [
        timestamp
        for timestamp in request_log[ip]
        if now - timestamp < WINDOW
    ]

    request_log[ip].append(now)

    count = len(request_log[ip])

    print(
        f"[MONITOR] {ip} -> {request.path} | "
        f"requests in {WINDOW}s: {count}"
    )

    if count > ALERT_THRESHOLD:
        print(
            f"[ALERT] High request rate detected from {ip}"
        )


@app.route("/")
def home():
    return "Vulnerable RCE Lab Server"


@app.route("/execute")
def execute():
    command = request.args.get("cmd", "")

    if not command:
        return "No command provided", 400

    # Intentionally vulnerable endpoint.
    # Use only inside the isolated security lab.
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


if __name__ == "__main__":
    print("Ubuntu Target Server")
    print("Flask server running on port 5000")
    print("RCE laboratory endpoint: /execute")
    print("Request monitoring enabled")

    app.run(
        host="0.0.0.0",
        port=5000
    )