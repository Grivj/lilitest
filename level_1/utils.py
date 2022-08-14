from pathlib import PurePath

from models.log import Log


def save_log(log: Log, folder: PurePath = PurePath("parsed")) -> None:
    """
    Save the given log to the given folder where the filename is the log's UUID.
    """

    with open(folder / f"{str(log.id)}.json", "w") as f:
        f.write(log.to_json())
