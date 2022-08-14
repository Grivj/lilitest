import json
from uuid import UUID

from pydantic import BaseModel, validator

from models.service import Service


class LogInput(BaseModel):
    """
    Input model for a log. The str log is as follows:

    id=<UUID> service_name=<service> process=<service>.<pid>
    sample#load_avg_1m=<float> sample#load_avg_5m=<float>
    sample#<metric>=<float> ...
    """

    log: str

    @validator("log")
    def validate_log(cls, log):
        parts = log.split(" ")

        if not parts or len(parts) < 3:
            raise ValueError("The Log is not valid, it must have at least 3 parts")

        cls.validate_id(parts[0])
        service = cls.validate_service(parts[1])
        cls.validate_process(parts[2], service)

        if len(parts) > 3:
            # More parts are present, validate them
            cls.validate_samples(parts[3:])

        return log

    @staticmethod
    def validate_id(part: str) -> None:
        key, value = part.split("=")
        if key != "id":
            raise ValueError("The id part of a Log must start with id=<UUID>")
        try:
            UUID(value)
        except ValueError as e:
            raise ValueError("The id is not a valid UUID") from e

    @staticmethod
    def validate_service(part: str) -> str:
        key, value = part.split("=")
        if key != "service_name":
            raise ValueError(
                "The service_name part of a Log must start with service_name=<service>"
            )
        if value.lower() not in Service.__members__:
            raise ValueError(f"The service {value} is not a valid service")
        return value

    @staticmethod
    def validate_process(part: str, service: str) -> None:
        key, value = part.split("=")
        if key != "process":
            raise ValueError(
                "The process part of a Log must start with process=<service>.<pid>"
            )

        service_name, pid = value.split(".")
        if service_name != service:
            raise ValueError("The process's service does not match the service_name")
        if not pid.isdigit():
            raise ValueError("The process's pid is not a valid integer")

    @staticmethod
    def validate_samples(parts: list[str]) -> None:
        for part in parts:
            key, value = part.split("#")
            if not key.startswith("sample"):
                raise ValueError(
                    "The sample part of a Log must start with sample#<metric>"
                )
            metric, value = value.split("=")
            try:
                float(value)
            except ValueError as e:
                raise ValueError(
                    f"The sample value {value} for the metric {metric} is not a valid integer"
                ) from e


class Log(BaseModel):
    id: UUID
    service_name: str
    process: str
    samples: list[tuple[str, float]]

    @classmethod
    def from_str(cls, log_input: str) -> "Log":
        parts = log_input.split(" ")

        def get_id() -> UUID:
            return UUID(parts[0].split("=")[1])

        def get_service_name() -> str:
            return parts[1].split("=")[1]

        def get_process() -> str:
            return parts[2].split("=")[1]

        def get_samples() -> list[tuple[str, float]]:
            samples = []
            for part in parts[3:]:
                _, value = part.split("#")
                metric, value = value.split("=")
                samples.append((metric, value))
            return samples

        return cls(
            id=get_id(),
            service_name=get_service_name(),
            process=get_process(),
            samples=get_samples(),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Log":
        return cls(
            id=UUID(data["id"]),
            service_name=data["service_name"],
            process=data["process"],
            samples=[
                (k, float(v))
                for k, v in data.items()
                if k not in ["id", "service_name", "process"]
            ],
        )

    def to_dict(self) -> dict[str, str]:
        res = {
            "id": str(self.id),
            "service_name": self.service_name,
            "process": self.process,
        }

        for sample in self.samples:
            res[sample[0]] = str(sample[1])

        return res

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
