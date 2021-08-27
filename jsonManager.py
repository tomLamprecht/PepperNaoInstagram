import json

path = 'data/'

def loadUserdata():
    with open(path +'userdata.json') as login_file:
        login_data = json.load(login_file)
        return login_data

def loadCachedSession():
    with open(path + 'cachedSession.json') as cached_session_file:
        return json.load(cached_session_file)

def dumpCachedSession(dumpingObj):
    with open(path + 'cachedSession.json' , 'w') as output_file:
        json.dump(dumpingObj, output_file)

def loadImageRecognitionResults():
    with open(path + 'imageRecognitionData.json') as data_file:
        return json.load(data_file)

def dumpImageRecoginitionResults(dumpingObj):
    with open(path + 'imageRecognitionData.json', 'w') as data_file:
        json.dump(dumpingObj, data_file)
