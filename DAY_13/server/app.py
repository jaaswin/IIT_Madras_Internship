from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import time

app = Flask(__name__)

# ==================================================
# FILE STORAGE
# ==================================================

UPLOAD_FOLDER = "/app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==================================================
# RATE LIMITER
# ==================================================

# Identify each client using its IP address
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)


# ==================================================
# IDS REQUEST MONITORING
# ==================================================

# Store request timestamps for each client IP
request_times = {}

# Generate an alert when a client reaches
# this number of upload requests
ALERT_THRESHOLD = 5

# Monitoring time window
MONITOR_WINDOW = 60


@app.before_request
def monitor_requests():

    # Monitor only file-upload requests
    if request.path != "/upload":
        return

    client_ip = request.remote_addr

    current_time = time.time()

    # Create an empty list for a new client
    if client_ip not in request_times:
        request_times[client_ip] = []

    # Remove requests older than 60 seconds
    request_times[client_ip] = [
        timestamp
        for timestamp in request_times[client_ip]
        if current_time - timestamp < MONITOR_WINDOW
    ]

    # Add the current request
    request_times[client_ip].append(current_time)

    request_count = len(request_times[client_ip])

    # ----------------------------------------------
    # MONITORING LOG
    # ----------------------------------------------

    print(
        f"[MONITOR] Upload request #{request_count} "
        f"from {client_ip}",
        flush=True
    )

    # ----------------------------------------------
    # IDS ALERT
    # ----------------------------------------------

    if request_count == ALERT_THRESHOLD:

        print(
            f"[ALERT] Abnormal upload activity detected "
            f"from {client_ip} "
            f"({request_count} requests in 60 seconds)",
            flush=True
        )


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return "Machine 3 - Secure File Upload Server"


# ==================================================
# FILE UPLOAD API
# ==================================================

@app.route("/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload():

    client_ip = request.remote_addr

    # ----------------------------------------------
    # CHECK FILE
    # ----------------------------------------------

    if "file" not in request.files:

        return jsonify({
            "status": "error",
            "message": "No file provided"
        }), 400

    file = request.files["file"]

    filename = file.filename

    if not filename:

        return jsonify({
            "status": "error",
            "message": "Invalid filename"
        }), 400

    # ----------------------------------------------
    # SAVE FILE
    # ----------------------------------------------

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    # ----------------------------------------------
    # UPLOAD LOG
    # ----------------------------------------------

    print(
        f"[UPLOAD] File '{filename}' uploaded "
        f"from {client_ip}",
        flush=True
    )

    return jsonify({
        "status": "success",
        "message": "File uploaded successfully"
    })


# ==================================================
# RATE LIMIT ERROR / MITIGATION
# ==================================================

@app.errorhandler(429)
def rate_limit_handler(error):

    client_ip = request.remote_addr

    print(
        f"[MITIGATION] Excessive traffic blocked "
        f"from {client_ip}",
        flush=True
    )

    return jsonify({
        "status": "blocked",
        "message": "Rate limit exceeded"
    }), 429


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    print("----------------------------------------", flush=True)
    print("Machine 3 server started", flush=True)
    print("File upload service is running", flush=True)
    print("IDS monitoring enabled", flush=True)
    print(
        "Rate limit: 5 uploads per minute/client",
        flush=True
    )
    print("----------------------------------------", flush=True)

    app.run(
        host="0.0.0.0",
        port=5000
    )
