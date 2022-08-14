import time


def compute(payload: dict) -> dict:
    time.sleep(3)
    payload["slow_computation"] = "0.0009878"

    return payload
