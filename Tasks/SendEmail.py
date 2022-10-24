import requests


def send(message):
    url = 'https://da897d59ec3093f998d930d05ceb60e4.m.pipedream.net'
    msg = {'message': message}
    requests.post(url, data=msg)
