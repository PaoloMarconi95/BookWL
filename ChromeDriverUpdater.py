import wget
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom


# url='https://golang.org/dl/go1.17.3.windows-amd64.zip'
# get.download(url)
# https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.20/ with final version ?
# zip_name = chromedriver_win32.zip

def start_update():
    response = requests.get("https://chromedriver.storage.googleapis.com/")
    text_to_parse = response.text
    version_string = parse_response2(text_to_parse)


def get_version_number(st):



def parse_response2(text):
    p3 = minidom.parseString(text)
    tagnames = p3.getElementsByTagName('Key')
    keys = []
    for tag in tagnames:
        keys.append(get_version_number(tag.firstChild.data))


start_update()
