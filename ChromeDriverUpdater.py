import requests
from zipfile import ZipFile

BASE_ZIP_PATH = 'https://chromedriver.storage.googleapis.com/'
ZIP_FILE_NAME = 'chromedriver_win32.zip'
ZIP_LOCAL_FOLDER = 'C:/Users/paolo.marconi/Desktop/pha/'


def start_update():
    response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    zip_url = BASE_ZIP_PATH + response.text + '/' + ZIP_FILE_NAME
    req = requests.get(zip_url)
    print(zip_url)
    with open(get_zip_name(response.text), 'wb') as output_file:
        output_file.write(req.content)
    zf = ZipFile(get_zip_name(response.text), 'r')
    zf.extractall(ZIP_LOCAL_FOLDER)
    zf.close()


def get_zip_name(version):
    return ZIP_LOCAL_FOLDER + 'chromedriver_' + version + '.zip'


start_update()
