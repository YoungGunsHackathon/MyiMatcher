import numpy as np
from sklearn.manifold import TSNE
import json


class Matcher:

    def edit_topics(arr):
        ''' Encode topic array to binary vector
        '''
        zeros = np.zeros(20)
        for x in range(len(arr)):
            index = users.topics[x]
            zeros[index] = 1
        return zeros

    def __init__(self, users):
        attendants = []
        self.users = users
        for user in users:
            usr = json.dumps(user)
            attendant = Attendant(usr['fname'], usr['lname'], self.edit_topics['topics'], self.edit_topics['career'])
            self.attendants.append(attendant)




    def test():
        return str(attendants[0].lname)


class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career
