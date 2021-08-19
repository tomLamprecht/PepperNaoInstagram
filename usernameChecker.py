from instagram_private_api import Client, ClientCompatPatch
import json
import time
class Checker:
    

    user_name = 'tomtestaccount1234'
    password = '09333575'

    def __init__(self):
        with open('data.txt') as json_file:
            cached_settings = json.load(json_file)
            self.api = Client(self.user_name, self.password, settings = cached_settings)


    #Checks if the Username exists
    # returns True if it exists and False if not
    def checkUsername(self, username):
        try:
            self.api.username_info(username)
            return True
        except Exception, e:
            return False


    def getRealName(self, username):
        return api.username_info(username)['user']['full_name']