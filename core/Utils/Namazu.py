import requests
from core.Utils.Config import config

host = config.get('Namazu', 'hostName')
port = config.get('Namazu', 'port')


def send(text):
    if host and port:
        return requests.post("http://{}:{}/command".format(host, port), text)


def use_skill(name):
    return send(("/ac " + str(name)).encode('utf-8'))
