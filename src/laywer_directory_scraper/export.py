import csv
import json
from pathlib import Path

from .lawyer import Lawyer

FIELD_NAMES = ["name", "bar_number", "address", "office_phone", "cell_phone", "email"]


def save_to_csv(lawyers: list[Lawyer], path: str | Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for lawyer in lawyers:
            writer.writerow(lawyer.to_dict())


def save_to_json(lawyers: list[Lawyer], path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([lawyer.to_dict() for lawyer in lawyers], f, indent=2)
