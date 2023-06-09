import requests
from zipfile import ZipFile
import json
import os
import Log
import pathlib

log = Log.logger

BASE_ZIP_PATH = 'https://chromedriver.storage.googleapis.com/'
ZIP_FILE_NAME = 'chromedriver_win32.zip'

def update_chromedriver():
    log.info('Updating chromedriver...')
    chromedriver_folder = get_chromedriver_folder()
    response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    zip_url = BASE_ZIP_PATH + response.text + '/' + ZIP_FILE_NAME
    req = requests.get(zip_url)

    # If there's a previous version of chromedriver.exe, remove it
    if os.path.isfile(chromedriver_folder + 'chromedriver.exe'):
        log.info('Deleting old chromedriver...')
        os.remove(chromedriver_folder + 'chromedriver.exe')

    with open(get_zip_name(response.text), 'wb') as output_file:
        log.info('Saving new chromedriver...')
        output_file.write(req.content)
        log.info(f'New chromedriver saved in selected folder: {get_zip_name(response.text)}')
    zf = ZipFile(get_zip_name(response.text), 'r')
    zf.extractall(chromedriver_folder)
    zf.close()
    return True


def get_zip_name(version):
    return get_chromedriver_folder() + 'chromedriver_' + version + '.zip'

def get_chromedriver_folder():
    f = open(os.path.join(pathlib.Path(__file__).parent.parent.resolve(), "config.json"), 'r')
    data = json.load(f)
    f.close()
    return data["CHROMEDRIVER_FOLDER"]
