import requests
import time

TARGET = "http://192.168.56.101:5000/"

for i in range(20):
    try:
        response = requests.get(TARGET, timeout=2)
        print(i + 1, response.status_code)

    except Exception as e:
        print("Error:", e)

    time.sleep(0.5)
    