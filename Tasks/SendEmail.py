import requests
import Log
import Configuration

conf = Configuration.conf
log = Log.logger

def send_from_url(message):
    msg = {'message': message}
    requests.post(conf["PIPEDREAM_MAIL_WF"], data=msg)
