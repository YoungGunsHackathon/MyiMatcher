import numpy as np
from flask import Flask, render_template
import urllib.request
import requests
import json
from urllib.parse import quote
from flask_bootstrap import Bootstrap
import binascii, os
from matcher import Matcher
from loop import create_intro_msg, create_suggestion_msg, connected

app = Flask(__name__)
Bootstrap(app)

BASE_URL = 'https://svc.hackathon.getmyia.com/hackathon/'
EVENT_ID = 'd4b90c0d-9862-4916-8190-335803032238eve' #'a49270cb-43b8-47fd-9b38-7bee69bc3dbaeve'
LAST_TIMESTAMP = str(636544271663550596)
TOKEN = '95811c85-6872-4127-bebb-8c0417ed3c3dtkn'
BOT_DEVICE_ID = '3bbe0ed2-91ac-4c77-b79d-9b5abb7e822a'
THREAD_ID_DICT = {}

def add_to_dict(key, value):
    ''' Function for updating user:thread dictionary
    '''
    THREAD_ID_DICT[key] = value

@app.route('/test')
def test():
    match = Matcher(get_all_users('new'))
    return match.test()

@app.route('/respond/<recipient_id>')
def respond(recipient_id):
    create_message(connected(), 'e06c8ebc-533e-4430-8e6b-60eaa56d455fthr')
    return 'OK'

@app.route('/chatbot_connect')
def chatbot_connect():
    ''' Function for creating chatbot and storing its ID, only called once per event
    '''
    DEVICE_ID = binascii.hexlify(os.urandom(16)).decode('ascii')

    payload = {
        "token": TOKEN,
        "deviceId": DEVICE_ID,
        "name": "Lovely Myia"
    }
    BOT_DEVICE_ID = DEVICE_ID
    r = requests.post(url = BASE_URL + 'chatbotconnect', json=payload)
    if r.status_code is not 200:
        raise API_Exception
    return 'OK'

@app.route('/create_thread/<recipient_id>')
def create_thread(recipient_id):
    ''' Function for creating thread between bot and attendant
    '''
    payload = {
        'deviceId': BOT_DEVICE_ID,
        'withProfileId': recipient_id
    }

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url = BASE_URL + 'place/' + EVENT_ID + '/thread', json = payload)
    if r.status_code is not 200:
        raise API_Exception
    add_to_dict(recipient_id, json.loads(r.text)['threadId'])
    return json.loads(r.text)['threadId']

@app.route('/create_message/<message>/<thread_id>')
def create_message(message, thread_id):
    ''' Function for pushing message to thread
    '''

    payload = {
        'deviceId': BOT_DEVICE_ID,
        'text': message,
        'linkId': binascii.hexlify(os.urandom(16)).decode('ascii')
    }
    r = requests.post(url = BASE_URL + 'place/' + EVENT_ID + '/thread/' + thread_id + '/message', json=payload)
    if r.status_code is not 200:
        return str(message)
    return 'OK'



@app.route('/match/<user_id>')
def match(user_id):
    ''' Endpoint for matching desired user with closest attendants
    '''
    # TODO MAGIC
    # Call function from matcher.py


# if when == now , return only new, when all, return all
@app.route('/get_all_users/<when>')
def get_all_users(when):
    ''' Endpoint for retrieving all users and their informations as Attendant class
    '''
    if when == 'new':
        ids = get_users_id_ts(LAST_TIMESTAMP)
    else:
        ids = get_users_id()
    ids = json.loads(ids)
    attendants = []

    for attendant_id in ids['profileIds']:
        try:
            details = json.loads(get_user_detail(attendant_id))
            fname = details['items'][1]['value']
            lname = details['items'][2]['value']
            topics = details['items'][3]['value']
            career = details['items'][4]['value']
            user_id = attendant_id
        except IndexError:
            continue
            #return str('User with id {} has not filled every detail'.format(attendant_id))

        attendant = Attendant(fname, lname, topics, career, user_id)
        attendants.append(attendant)

    return json.dumps([ob.__dict__ for ob in attendants])


@app.route("/num_of_attendants")
def num_of_attendants():
    ''' Endpoint for retrieving number of people attending Event
    '''
    ids = get_users_id()
    ids = json.loads(ids)
    return len(ids['profileIds'])

@app.route("/")
def hello():
    ''' Main endpoint at / for dashboard UI
    '''
    return render_template('dashboard.html', event={'num': num_of_attendants()})

@app.route("/get_users_id")
def get_ids():
    ''' Endpoint for retrieving all ids of users attending current event
    '''
    return get_users_id()

@app.route('/get_user_details/<user_id>')
def get_details(user_id):
    ''' Endpoint for retrieving information about user according to his id
    '''
    return get_user_detail(user_id)


def get_user_detail(user_id):
    ''' Function for retrieving informations about the selected user
        attending event
    '''
    url = 'https://svc.hackathon.getmyia.com/hacklathon/' + 'profilex/' + user_id + '/' + EVENT_ID + '/json'
    user_info = requests.get(url)
    if user_info.status_code is not 200:
        raise API_Exception
    return user_info.content.decode('utf-8')


def get_users_id():
    ''' Function for retrieving users that are attending
    '''
    users_id = requests.get(BASE_URL + 'place/' + EVENT_ID + '/activeusers')
    if users_id.status_code is not 200:
        raise API_Exception
    res = users_id.content.decode('utf-8')
    LAST_TIMESTAMP = json.loads(res)['lastStamp']
    return res

def get_users_id_ts(timestamp):
    ''' Function for retrieving new users after time defined in timestamp
    '''
    users_id = requests.get(BASE_URL + 'place/' + EVENT_ID + '/activeusers?lastStamp=' + timestamp)
    if users_id.status_code is not 200:
        raise API_Exception
    res = users_id.content.decode('utf-8')
    LAST_TIMESTAMP = json.loads(res)['lastStamp']
    return res


class API_Exception(Exception):
    pass

class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career, user_id):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career
        self.user_id = user_id

#d
# 0.0.0.0 so it can be visible from local network
message = '''
Chcete propojit s p. Novakem?
<div style="margin-top: 10px"><button style="background: #222 url('css/themes/dark/img/voteUp.svg') no-repeat center center;background-size:64px 64px;width:55px;height:55px;padding: 0;margin-right: 10px;display:inline-block" onclick="this.style.backgroundImage = 'url(css/themes/dark/img/voteUpSelected.svg)';angular.element(document.body).injector().get('xinClientService').getData('https:'+'//centrum.cz', 'GET')"></button><button style="background: #222 url('css/themes/dark/img/voteDown.svg') no-repeat center center;background-size:64px 64px;width:55px;height:55px;padding: 0;margin-right: 10px;display:inline-block" onclick="this.style.backgroundImage = 'url(css/themes/dark/img/voteDownSelected.svg)';angular.element(document.body).injector().get('xinClientService').getData('https:'+'//centrum.cz', 'GET')"></button></div>
'''

create_message(create_suggestion_msg('e06c8ebc-533e-4430-8e6b-60eaa56d455fthr','Josef', 'Neco', 'Neco2', 'Neco3', 1), 'e06c8ebc-533e-4430-8e6b-60eaa56d455fthr')

app.run(debug=True, host='0.0.0.0')
