from pathlib import Path
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
import os
from dataclasses import dataclass


@dataclass()
class Configuration(YamlDataClassConfig):
    signin_url: str = None
    calendar_url: str = None
    chromedriver_folder: str = None
    gmail_key: str = None
    html_file_path: str = None
    png_file_path: str = None
    calendar_el_id: str = None
    cookie_path: str = None
    db_path: str = None
    max_login_attempts: int = 5
    sign_in_delta: int = 10
    FILE_PATH: Path = create_file_path_field(os.path.join(Path(__file__).parent, 'configuration_new.yaml'))
