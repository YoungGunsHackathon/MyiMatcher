import numpy as np
from flask import Flask
import urllib.request
import requests
import json


app = Flask(__name__)


BASE_URL = 'http://svc.hackathon.getmyia.com/hackathon/'
EVENT_ID = 'a49270cb-43b8-47fd-9b38-7bee69bc3dbaeve'


@app.route('/get_all_users')
def get_all_users():
    ''' Endpoint for retrieving all users and their informations as Attendant class
    '''
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
        except IndexError:
            return str('User with id {} has not filled every detail'.format(attendant_id))

        attendant = Attendant(fname, lname, topics, career)
        attendants.append(attendant)

    return json.dumps([ob.__dict__ for ob in attendants])
    

@app.route("/")
def hello():
    return 'Yep im working'

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
    return users_id.content.decode('utf-8')


class API_Exception(Exception):
    pass

class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career


# 0.0.0.0 so it can be visible from local network
app.run(debug=True, host='0.0.0.0')
