# Level 1 explanation

## Routes

This simple FastAPI REST API serves two default routes:

- _GET_ `/`: returns a list of logs UUIDs saved on the server
- _POST_ `/`: creates a log from the given string with following format:

```text
id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 sample#load_avg_15m=0.202
```

- _GET_ `/logs/{uuid}`: returns the log with the given UUID

## Starting the app

To start the container and the app, run the following command from the root path of the main folder:

```bash
docker-compose up api-level-1
```

Doing so will start the app on `localhost:3000`.

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

The log_generator will occasionally fail to push a log thus printing a 422 response (Unprocessable Entity) like seen above for log #3. This is due to the fact that 1/10 are badly generated, e.g., the uuid part is prefixed with a blank space (see `log_generator.py` line `6` and `10`).

### Showcase

#### `/`

```bash
curl -X 'GET' 'http://127.0.0.1:3000/' -H 'accept: application/json'
```

```json
Code 200
```

```json
{
  "logs": [
    "232ad25d-e677-458d-a7ed-2f7cae161b19.json",
    "caebc4d7-cdb1-4323-bdc2-77c77c60ead7.json",
    "6be1ec31-bb16-467d-9ec3-d34039db9b9c.json",
    "4ebca425-ad37-429d-bb13-d0cc03485302.json",
    "e12f0cdc-9706-4b5b-85e3-eafa25b4a3f2.json",
    "7d36198f-d2b8-4c9d-889e-dc1c6a63e230.json",
    "dad7f673-9544-411a-b25c-e92a27a30f8b.json",
    "36af37b3-fab3-486e-ab69-d3dfd6b03547.json",
    "e66fd9e8-9671-4bdc-9315-be1677d434fc.json",
    "74764b1a-fe7c-465d-9a56-d1aba53b3141.json"
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

#### `/logs/{uuid}`

```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/logs/de9565ce-56cf-4e9e-98ec-2c76487be251' \
  -H 'accept: application/json'
```

```json
Code 200
```

```json
{
  "id": "de9565ce-56cf-4e9e-98ec-2c76487be251",
  "service_name": "admin",
  "process": "admin.3298",
  "samples": [
    ["load_avg_1m", 0.113],
    ["load_avg_5m", 0.365],
    ["load_avg_15m", 0.922]
  ]
}
```
