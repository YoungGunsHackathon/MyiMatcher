import numpy as np
from flask import Flask
import urllib.request
import requests


app = Flask(__name__)


BASE_URL = 'http://svc.hackathon.getmyia.com/hackathon/'
EVENT_ID = 'd2999e59-82bb-4980-81f7-61d2115a4412eve'


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
    user_info = requests.get(BASE_URL + 'profiles/' + EVENT_ID + '/' + user_id + '/json')
    if user_info.status_code is not 200:
        raise API_Exception
    return user_info.content


def get_users_id():
    ''' Function for retrieving users that are attending
    '''
    users_id = requests.get(BASE_URL + 'place/' + EVENT_ID + '/activeusers')
    if users_id.status_code is not 200:
        raise API_Exception
    return users_id.content


class API_Exception(Exception):
    pass

# 0.0.0.0 so it can be visible from local network
app.run(debug=True, host='0.0.0.0')
