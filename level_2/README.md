# Level 2 explanation

## Routes

This simple FastAPI REST API serves two default routes:

- _GET_ `/`: returns a list of logs UUIDs saved on the server
- _POST_ `/`: creates a log from the given string with following format:

```text
id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 sample#load_avg_15m=0.202
```

## Starting the app

To start the container and the app, run the following command from the root path of the main folder:

```bash
docker-compose up --build api-level-2
```

Doing so will start the app on `localhost:3000` and will also create the
container for Redis, which is used for this test level.

## Running the test

To run the test, run the following command from the root path of the main folder:

```bash
python levels_http
```

This should start the generation of logs and push them to `localhost:3000/`. The console should attest that the logs are being pushed by printing the `status_code` of the response and the index of the log pushed, like so:

```text
201 1/1000
201 2/1000
422 3/1000
201 4/1000
201 5/1000
201 6/1000
201 7/1000
201 8/1000
201 9/1000
201 10/1000
```

## Failing requests

- The log_generator will occasionally fail to push a log thus printing a 422 response (Unprocessable Entity) like seen above for log #3. This is due to the fact that 1/10 are badly generated, e.g., the uuid part is prefixed with a blank space (see `log_generator.py` line `6` and `10`).
- One of the complexity of the test is that requests timeout after 100 milliseconds, so the test will fail because of the `slow_computation.compute` task. To fix the issue, the task is run in the background as well as the saving of the log to redis. That way, if either the compute or the saving takes longer than 100 milliseconds, the request will not timeout and will still be `200`. Unless, of course, there are problems with the initial query.

### Showcase

#### `/`

```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/?start=0&end=10' \
  -H 'accept: application/json'
```

```json
Code 200
```

```json
{
  "number_of_logs": 900,
  "start": 10,
  "end": 20,
  "number_of_selected_logs": 10,
  "remaining": 880,
  "logs": [
    {
      "id": "c533ed5e-7caf-4243-85c3-16a2e4a07c67",
      "service_name": "admin",
      "process": "admin.2136",
      "samples": [
        ["load_avg_1m", 0.207],
        ["load_avg_5m", 0.619],
        ["load_avg_15m", 0.942],
        ["slow_computation", 0.0009878]
      ]
    },
    {
      "id": "910a3e04-17d9-4a8c-9018-9e61de13d6ae",
      "service_name": "admin",
      "process": "admin.3803",
      "samples": [
        ["load_avg_1m", 0.113],
        ["load_avg_5m", 0.864],
        ["load_avg_15m", 0.869],
        ["slow_computation", 0.0009878]
      ]
    },
    ...
  ]
}
```

---

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "log": "id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 sample#load_avg_15m=0.202"
}'
```

```json
Code 201
```

```json
null
```
