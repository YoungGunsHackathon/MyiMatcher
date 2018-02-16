import numpy as np
from sklearn.manifold import TSNE
import json


class Matcher:

    def edit_topics(self, arr):
        ''' Encode topic array to binary vector
        '''
        zeros = np.zeros(20)
        for x in range(len(arr)):
            index = arr[x]
            zeros[index] = 1
        return zeros

    def __init__(self, users):
        self.users = self.objects_from_json(users)
        for user in self.users:
            user.topics = self.edit_topics(user.topics)

    def objects_from_json(self, raw):
        ''' Function for creating objects from json
        '''
        js = raw.replace("\\", "")
        js = json.loads(js)
        attendants = []
        for x in range(len(js)):
            attendants.append(Attendant(js[x]['fname'], js[x]['lname'], js[x]['topics'], js[x]['career']))
        return attendants

    def test(self):
        return str(self.users[0].topics)


class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career
