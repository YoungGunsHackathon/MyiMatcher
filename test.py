import json
jsonn = "[{\"lname\": \"Redman\", \"career\": [0, 3], \"fname\": \"Luis\", \"topics\": [16, 6, 8, 0, 5]}, {\"lname\": \"Do\", \"career\": [0], \"fname\": \"Loi\", \"topics\": [5, 9, 11]}, {\"lname\": \"Kerous\", \"career\": [4], \"fname\": \"Bolek\", \"topics\": [1, 2, 5, 7, 10, 12, 15, 18]}]"


def objects_from_json(raw):
    js = raw.replace("\\", "")
    js = json.loads(js)
    attendants = []
    for x in range(len(js)):
        attendants.append(Attendant(js[x]['fname'], js[x]['lname'], js[x]['topics'], js[x]['career']))
    return attendants

class Attendant:
    ''' Data class representing one event Attendant
    '''
    def __init__(self, fname, lname, topics, career):
        self.fname = fname
        self.lname = lname
        self.topics = topics
        self.career = career

a = objects_from_json(jsonn)
print(a[0].fname)
