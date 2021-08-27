from instagram_private_api import Client, ClientCompatPatch
import json
import time
import jsonManager
class Checker:
    

    login_data = jsonManager.loadUserdata()
    user_name = login_data['username']
    password = login_data['password']

    def __init__(self):
        cached_settings = jsonManager.loadCachedSession()
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