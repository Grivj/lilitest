from uuid import UUID

import pytest
from models.log import Log, LogInput


def test_log_input_validate_id():
    # valid prefix and id
    assert LogInput.validate_id("id=4755dc84-4621-4ba9-a83d-136080aae309") is None

    # missing id= part
    with pytest.raises(ValueError):
        LogInput.validate_id("4755dc84-4621-4ba9-a83d-136080aae309")

    # not a valid UUID
    with pytest.raises(ValueError):
        LogInput.validate_id("id=4755dc84-4621-4ba9-a83d")


def test_log_input_validate_service():
    # valid service
    assert LogInput.validate_service("service_name=api") == "api"

    # missing service_name= part
    with pytest.raises(ValueError):
        LogInput.validate_service("service")

    # not a valid service
    with pytest.raises(ValueError):
        LogInput.validate_service("service_name=service1")


def test_log_input_validate_process():
    # valid process
    assert LogInput.validate_process("process=api.1", "api") is None

    # missing process= part
    with pytest.raises(ValueError):
        LogInput.validate_process("api.1", "api")

    # not a valid process
    with pytest.raises(ValueError):
        LogInput.validate_process("process=service.1", "service1")

    # process service is not the same as service_name
    with pytest.raises(ValueError):
        LogInput.validate_process("process=api.1", "service")


def test_log_input_validate_samples():
    # valid samples
    assert LogInput.validate_samples(["sample#cpu=1", "sample#memory=2"]) is None

    # missing sample# part
    with pytest.raises(ValueError):
        LogInput.validate_samples(["cpu=1", "memory=2"])

    # not a valid metric
    with pytest.raises(ValueError):
        LogInput.validate_samples(["sample#cpu=1", "sample#memory"])


def test_log_from_str():
    str_log = "id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 sample#load_avg_5m=0.561 sample#load_avg_15m=0.202"
    log = Log.from_str(str_log)
    assert log.id == UUID("0060cd38-9dd5-4eff-a72f-9705f3dd25d9")
    assert log.service_name == "api"
    assert log.process == "api.233"
    assert log.samples == [
        ("load_avg_1m", 0.849),
        ("load_avg_5m", 0.561),
        ("load_avg_15m", 0.202),
    ]


def test_log_from_dict():
    dict_log = {
        "id": "0060cd38-9dd5-4eff-a72f-9705f3dd25d9",
        "service_name": "api",
        "process": "api.233",
        "load_avg_1m": 0.849,
        "load_avg_5m": 0.561,
        "load_avg_15m": 0.202,
    }
    log = Log.from_dict(dict_log)
    assert log.id == UUID("0060cd38-9dd5-4eff-a72f-9705f3dd25d9")
    assert log.service_name == "api"
    assert log.process == "api.233"
    assert log.samples == [
        ("load_avg_1m", 0.849),
        ("load_avg_5m", 0.561),
        ("load_avg_15m", 0.202),
    ]
