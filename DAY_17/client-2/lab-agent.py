from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/")
def home():
    return "Client 2 Lab Agent"


@app.route("/start-test")
def start_test():
    subprocess.Popen(["python3", "traffic-test.py"])
    return "Controlled lab traffic started"


if __name__ == "__main__":
    print("Client 2 Lab Agent")
    print("Listening on port 6000")

    app.run(
        host="0.0.0.0",
        port=6000
    )