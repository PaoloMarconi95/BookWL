from datetime import datetime, timedelta
from dataclasses_json import dataclass_json
from pathlib import Path
from typing import List, Optional
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass, field


@dataclass_json()
@dataclass()
class Booking:
    class_name: str = None
    class_time: int = None
    week_day: int = None
    date: Optional[str] = None

    def __post_init__(self):
        self.date = get_closer_date_with_weekday(self.week_day)


@dataclass_json()
@dataclass()
class User:
    name: str = None
    username: str = None
    pwd: str = None
    bookings: Optional[List[Booking]] = field(default_factory=list)


@dataclass()
class Configuration(YamlDataClassConfig):
    signin_url: str = None
    calendar_url: str = None
    chromedriver_folder: str = None
    platform: str = None
    users: Optional[List[User]] = field(default_factory=list)
    gmail_key: str = None
    html_file_path: str = None
    calendar_el_id: str = None
    max_login_attempts: int = 3
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'configuration.yaml'))


def get_closer_date_with_weekday(week_day):
    if not(0 <= week_day <= 6):
        raise ValueError("Week Day " + str(week_day) + "Invalid!")
    else:
        today_week_day = datetime.today().weekday()
        delta = 7 + (week_day - today_week_day)
        final_date = datetime.today() + timedelta(days=delta)
        return datetime.strftime(final_date, "%d-%m-%Y")
