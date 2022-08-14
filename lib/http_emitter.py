import uuid

import requests

import lib.log_generator as log_generator

ENDPOINT = "http://127.0.0.1:3000"

for i in range(1000):
    try:
        req = requests.post(
            ENDPOINT, json={"log": log_generator.sample(uuid.uuid4())}, timeout=0.1
        )

        print(f"{req.status_code} {i + 1}/1000")
    except requests.Timeout:
        print(f"Remote server timed-out on {ENDPOINT}")
    except requests.ConnectionError:
        print(f"Connection refused on {ENDPOINT}")
