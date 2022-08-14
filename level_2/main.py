import json

from fastapi import BackgroundTasks, FastAPI
from redis import Redis

from models.log import Log, LogInput
from slow_computation import compute

app = FastAPI()


@app.on_event("startup")
def startup():
    app.redis = Redis(host="level-2-redis", port=6379)


@app.get("/")
def read_logs(start: int = 0, end: int = 10):
    n_logs = app.redis.llen("logs")
    return {
        "number_of_logs": n_logs,
        "start": start,
        "end": end,
        "number_of_selected_logs": min(end, n_logs) - start,
        "remaining": n_logs - end,
        "logs": [
            Log.from_dict(json.loads(log))
            for log in app.redis.lrange("logs", start, end)
        ],
    }


@app.post("/", status_code=201)
async def create_log(log_input: LogInput, background_tasks: BackgroundTasks):
    """
    Receives a log in string format such as:
        id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233
        sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 [...],
    parse it and perform some slow computation. Finally, save the log (with the
    result of the computation) in a Redis list.

    * The saving task is done in the background to not block the response.
    """

    log = Log.from_str(log_input.log)

    # call the slow computation function and save the result in the Redis list
    # * Ideally, this would be done in a separate process, but I keep things
    # * simple here to only use the BackgroundTasks feature.
    def slow_compute_with_redis_push(log: Log):
        result = compute(log.to_dict())
        app.redis.lpush("logs", json.dumps(result))

    background_tasks.add_task(slow_compute_with_redis_push, log)
