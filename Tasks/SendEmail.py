import requests

class Email:
    def __init__(self, url = 'https://da897d59ec3093f998d930d05ceb60e4.m.pipedream.net'):
        self.url = url
        super(self)

    def send_from_url(self, message):
        msg = {'message': message}
        requests.post(self.url, data=msg)
