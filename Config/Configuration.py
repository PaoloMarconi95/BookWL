from datetime import datetime, timedelta
from dataclasses_json import dataclass_json
from pathlib import Path
from typing import List, Optional
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass, field


@dataclass()
class Configuration(YamlDataClassConfig):
    signin_url: str = None
    calendar_url: str = None
    chromedriver_folder: str = None
    platform: str = None
    gmail_key: str = None
    html_file_path: str = None
    calendar_el_id: str = None
    db_path: str = None
    max_login_attempts: int = 3
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'configuration.yaml'))
