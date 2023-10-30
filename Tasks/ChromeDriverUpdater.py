import requests
from zipfile import ZipFile
import json
import os
from Config import LOGGER, CONFIG


def update_chromedriver():
    LOGGER.info('Updating chromedriver...')
    response = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
    latest_releases = json.loads(response.text)
    stable_version = latest_releases['channels']['Stable']['version']
    chromedrivers_zip = latest_releases['channels']['Stable']['downloads']['chromedriver']
    chromedrivers_zip_platform = filter(lambda x: x['platform'] == CONFIG.platform, chromedrivers_zip)
    url_chromedriver = list(chromedrivers_zip_platform)[0]['url']
    downloaded_zip = requests.get(url_chromedriver)

    # If there's a previous version of chromedriver.exe, remove it
    abs_path_file = os.path.join(CONFIG.chromedriver_folder, 'chromedriver.exe')
    if os.path.isfile(abs_path_file):
        LOGGER.info('Deleting old chromedriver...')
        os.remove(abs_path_file)

    with open(get_zip_name(stable_version), 'wb') as output_file:
        LOGGER.info('Saving zip')
        output_file.write(downloaded_zip.content)
        LOGGER.info(f'New chromedriver saved in selected folder: {get_zip_name(stable_version)}')

    zf = ZipFile(get_zip_name(stable_version), 'r')
    LOGGER.info('Extracting zip...')
    zf.extractall(path=get_unzipped_folder_name(stable_version))
    zf.close()


    # Move main chromedriver.exe to main CHROMEDRIVER_FOLDER
    LOGGER.info('Moving zip to main folder...')
    os.rename(os.path.join(get_unzipped_folder_name(stable_version), f"chromedriver-{CONFIG.platform}/chromedriver.exe"),
              os.path.join(CONFIG.chromedriver_folder, 'chromedriver.exe' if os.name == 'nt' else 'chromedriver'), )
    return True


def get_zip_name(version):
    return os.path.join(CONFIG.chromedriver_folder, f"chromedriver_{version}.zip")


def get_unzipped_folder_name(version):
    return os.path.join(CONFIG.chromedriver_folder, f"chromedriver_{version}")


def get_latest_chromedriver_version():
    response = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
    latest_releases = json.loads(response.text)
    stable_version = latest_releases['channels']['Stable']['version']
    return stable_version
