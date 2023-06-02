import requests
import Log
import Configuration

config = Configuration.global_config
log = Log.logger

def send_from_url(message):
    msg = {'message': message}
    requests.post(config.pipedream_mail, data=msg)
