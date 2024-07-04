from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from dataclasses_json import dataclass_json
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass


@dataclass_json()
@dataclass(init=False)
class ClassToBeBooked:
    user_id: int = None
    name: str = None
    program: str = None
    time: str = None
    week_day: int = None
    date: Optional[datetime] = None

    def __init__(self, user_id, name, program, time, week_day, date):
        self.user_id = user_id
        self.name = name
        self.program = program
        self.time = time
        self.week_day = week_day

        today = datetime.now()
        days_ahead = week_day - today.weekday()
        if days_ahead <= 0:  # If the target day has passed this week, go to the next week
            days_ahead += 7
        date = today + timedelta(days=days_ahead)
        minute = time[3:] if time[3:] != '00' else 0
        hour = time[:2] if time[0] != 0 else int(time[1])
        self.date = date.replace(hour=int(hour), minute=int(minute), second=0)


@dataclass()
class FutureBookingConfiguration(YamlDataClassConfig):
    classes: list[ClassToBeBooked] = None
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'FutureBookingConfiguration.yaml'))
