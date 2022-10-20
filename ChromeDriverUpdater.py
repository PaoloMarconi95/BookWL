import requests
from zipfile import ZipFile
import os

# noinspection PyPep8Naming
from Log import Log as LOG

BASE_ZIP_PATH = 'https://chromedriver.storage.googleapis.com/'
ZIP_FILE_NAME = 'chromedriver_win32.zip'
CHROMEDRIVER_FOLDER = 'C:/Users/Public/Selenium/'


def update_chromedriver():
    LOG.info('Updating chromedriver...')
    response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    zip_url = BASE_ZIP_PATH + response.text + '/' + ZIP_FILE_NAME
    req = requests.get(zip_url)

    # If there's a previous version of chromedriver.exe, remove it
    if os.path.isfile(CHROMEDRIVER_FOLDER + 'chromedriver.exe'):
        os.remove(CHROMEDRIVER_FOLDER + 'chromedriver.exe')

    with open(get_zip_name(response.text), 'wb') as output_file:
        output_file.write(req.content)
        LOG.info('New chromedriver saved in selected folder')
    zf = ZipFile(get_zip_name(response.text), 'r')
    zf.extractall(CHROMEDRIVER_FOLDER)
    zf.close()
    return True


def get_zip_name(version):
    return CHROMEDRIVER_FOLDER + 'chromedriver_' + version + '.zip'
