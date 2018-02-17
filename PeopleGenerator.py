placeToken = "2fadf2df-5f38-4736-872a-6a063ee6b031tkn"
placeId = "cb979966-6190-4d97-be3d-a550602cc0b7eve"
baseConnectURL = "https://svc.hackathon.getmyia.com/hackathon/connect"
baseProfileSetURL = "https://svc.hackathon.getmyia.com/hackathon/myprofile/cs"


import names
import requests
import random
import numpy as np
import numpy.random as npr
from scipy import stats

def getRandomInterestDistr():
    return npr.choice(numpy.arange(0, 20), p=[1/52, 1/52, 7/52, 2/52, 1/52, 2/52, 2/52, 7/52, 2/52, 1/52, 1/52, 2/52, 1/52, 1/52, 8/52, 1/52, 2/52, 2/52, 5/52, 3/52])


def getInterestArray():
    #return random.sample(range(0, 20), random.randint(1,5))
    array = [None] * random.randint(1,5)
    for i in range(0, array.__len__()):
        array[i] = int(getRandomInterestDistr())
    return array


print(getInterestArray())

def getCarArray():
    chance = npr.rand()
    if(chance > 0.80):
        return [4]
    elif(chance > 0.30):
        return random.sample(range(0,4), random.randint(1,2))
    else:
        return random.sample(range(0,4), random.randint(1,4))


def getRandomUser(devId):

    firstName = names.get_first_name()
    lastName = names.get_last_name()

    return {
        'deviceId': devId,
        'placeId': placeId,
        'items': [
            {
                'id': 0,
                'caption': 'Photo',
                'type': 2,
                'semanticType': 4,
                'value': 'https://source.unsplash.com/random/400x400?sig=123'
            },
            {
                'id': 1,
                'caption': 'First name',
                'type': 0,
                'semanticType': 1,
                'value': firstName
            },
            {
                'id': 2,
                'caption': 'Last name',
                'type': 0,
                'semanticType': 2,
                'value': lastName
            },
            {
                'id': 5,
                'caption': 'Field of Interest',
                'type': 4,
                'semanticType': 0,
                'value': getInterestArray(),
                'selectOptions': [
                    {
                        'id': 0,
                        'value': '3D Printing'
                    },
                    {
                        'id': 1,
                        'value': 'Aerospace Engineering'
                    },
                    {
                        'id': 2,
                        'value': 'Artificial Intelligence'
                    },
                    {
                        'id': 3,
                        'value': 'Augmented Reality'
                    },
                    {
                        'id': 4,
                        'value': 'Biotechnology'
                    },
                    {
                        'id': 5,
                        'value': 'Blockchain'
                    },
                    {
                        'id': 6,
                        'value': 'Brain-computer interface'
                    },
                    {
                        'id': 7,
                        'value': 'Business'
                    },
                    {
                        'id': 8,
                        'value': 'Cyber Security'
                    },
                    {
                        'id': 9,
                        'value': 'Data Science'
                    },
                    {
                        'id': 10,
                        'value': 'Future of Education'
                    },
                    {
                        'id': 11,
                        'value': 'Future of Food'
                    },
                    {
                        'id': 12,
                        'value': 'Future of Health'
                    },
                    {
                        'id': 13,
                        'value': 'Genetics'
                    },
                    {
                        'id': 14,
                        'value': 'Internet of Things'
                    },
                    {
                        'id': 15,
                        'value': 'Nanotechnology'
                    },
                    {
                        'id': 16,
                        'value': 'Neuroscience'
                    },
                    {
                        'id': 17,
                        'value': 'Quantum computing'
                    },
                    {
                        'id': 18,
                        'value': 'Self-driving Cars'
                    },
                    {
                        'id': 19,
                        'value': 'Virtual Reality'
                    }
                ]
            },
            {
                'id': 6,
                'caption': 'Looking for:',
                'type': 4,
                'semanticType': 0,
                'value': getCarArray(),
                'selectOptions': [
                    {
                        'id': 0,
                        'value': 'Job'
                    },
                    {
                        'id': 1,
                        'value': 'Employees'
                    },
                    {
                        'id': 2,
                        'value': 'Investors'
                    },
                    {
                        'id': 3,
                        'value': 'Investment Opportunities'
                    },
                    {
                        'id': 4,
                        'value': 'N/A'
                    }
                ]
            }
        ],
        'nick': firstName + lastName
    }


import os
import json
import binascii

for i in range(0, 50):
    devId = binascii.hexlify(os.urandom(16)).decode('ascii')
    stringConnect = {'deviceId': devId, 'placeToken': placeToken}

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    r1 = requests.post(url = baseConnectURL, data=stringConnect)
    r2 = requests.post(url = baseProfileSetURL, json=getRandomUser(devId), headers = headers)
    print(r1.status_code)
    print(r2.status_code)
    print('---')