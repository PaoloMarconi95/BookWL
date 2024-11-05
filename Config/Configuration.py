from pathlib import Path

from dataclasses_json import dataclass_json
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass


@dataclass_json()
@dataclass()
class User:
    id: int = None
    name: str = None
    mail: str = None
    password: str = None


@dataclass()
class Configuration(YamlDataClassConfig):
    signin_url: str = None
    calendar_url: str = None
    login_url: str = None
    gmail_key: str = None
    png_file_path: str = None
    calendar_el_id: str = None
    max_login_attempts: int = None
    users: list[User] = None
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'configuration.yaml'))
