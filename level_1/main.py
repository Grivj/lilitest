import json
import os

from fastapi import BackgroundTasks, FastAPI, HTTPException

from models.log import Log, LogInput
from utils import save_log

app = FastAPI()


@app.get("/")
def read_logs():
    """Return a list of all the logs saved in the server's."""

    return os.listdir("parsed")


@app.post("/", status_code=201)
def create_log(log_input: LogInput, background_tasks: BackgroundTasks):
    """
    Receives a log in string format such as:
        id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233
        sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 [...],
    parse it and save it as JSON in the appropriate folder.

    * The saving task is done in the background to not block the response.
    """

    log = Log.from_str(log_input.log)
    background_tasks.add_task(save_log, log)


@app.get("/logs/{log_id}", response_model=Log)
def read_log(log_id: str):
    """Find a log saved in a JSON file via its UUID."""

    try:
        with open(f"parsed/{log_id}.json", "r") as f:
            return Log.from_dict(json.loads(f.read()))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Log not found") from e
