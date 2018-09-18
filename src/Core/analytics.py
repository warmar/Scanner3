import requests
import secrets
import time
import os

characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYXZ0123456789'

PATH = 'Resources/clientid'


def get_client_id():
    # Reads or creates random client id (anonymous)
    if os.path.exists(PATH):
        with open(PATH, 'r') as id_file:
            client_id = id_file.read()
        return client_id

    client_id = ''
    for _ in range(24):
        client_id += secrets.choice(characters)

    with open(PATH, 'w+') as id_file:
        id_file.write(client_id)

    return client_id

def report_launch():
    client_id = get_client_id()
    curr_time = round(time.time(), 2)
    try:
        requests.get('https://scanner3.net/analytics?id=%s&launchTime=%s' % (client_id, curr_time))
    except:
        pass


def report_close():
    client_id = get_client_id()
    curr_time = round(time.time(), 2)
    try:
        requests.get('https://scanner3.net/analytics?id=%s&closeTime=%s' % (client_id, curr_time))
    except:
        pass
