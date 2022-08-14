import random


def sample(uuid):
    service = random.choice(["web", "admin", "api"])
    errors = random.randint(0, 10)
    return " ".join(
        [
            f"id={uuid}" if errors != 0 else f"id= {uuid}",
            f"service_name={service}",
            f"process={service}.{random.randint(1, 4001)}",
            f"sample#load_avg_1m={round(random.random(), 3)}",
            f"sample#load_avg_5m={round(random.random(), 3)}",
            f"sample#load_avg_15m={round(random.random(), 3)}",
        ]
    )
