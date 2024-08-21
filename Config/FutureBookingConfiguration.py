from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses_json import dataclass_json
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass

from Model.BookingResult import BookingResult


@dataclass_json()
@dataclass(init=False)
class ClassToBeBooked:
    user_id: int = None
    name: str = None
    program: str = None
    time: str = None
    week_day: int = None
    date: Optional[datetime] = None
    booking_result: Optional[BookingResult] = None

    def __init__(self, user_id, name, program, time, week_day, date, booking_result):
        self.user_id = user_id
        self.name = name
        self.program = program
        self.time = time
        self.week_day = week_day
        self.date = None


@dataclass()
class FutureBookingConfiguration(YamlDataClassConfig):
    classes: list[ClassToBeBooked] = None
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'FutureBookingConfiguration.yaml'))
