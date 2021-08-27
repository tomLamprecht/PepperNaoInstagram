# This Python file uses the following encoding: utf-8

from instagram_private_api import Client, ClientCompatPatch
import json
import time
import urllib
import farewells
import comments
import os
import jsonManager

def interpretInstaPic(shortcode):
    os.system('py -3.7 imageRecognition.py --shortcode '+shortcode)

    with open("data/imageRecognitionData.json") as file:
        results = json.load(file)

    print(results[1]['prediction_translated'] + " " + str(results[1]['probability']) + '%')
    print(results[0]['prediction_translated'] + " " + str(results[0]['probability']) + '%')


def getFullName(name):
    url = "https://www.picuki.com/profile/"
    page = str(urllib.urlopen(url + name).read())
    search = '<h2 class="profile-name-bottom">'
    beg = page.index(search) + len(search)
    end = page.index("</", beg)
    return page[beg:end]


def getUserId(name):
    url = "https://www.picuki.com/profile/"
    page = str(urllib.urlopen(url + name).read())
    search = "let query = '"
    beg = page.index(search) + len(search)
    end = page.index("\';", beg)
    return page[beg:end]
    

def getMediaID(name):
    url = "https://www.picuki.com/profile/"
    page = str(urllib.urlopen(url + name).read())
    search = 'https://www.picuki.com/media/'
    beg = page.index(search) + len(search)
    end = page.index("\">", beg)
    return (page[beg:end])

#https://i.instagram.com/api/v1/users/48804734072/info/

#user_name = 'tomtestaccount1234'
tamiUserId = '1590709555'
main_username = "tom_15_01"
#password = '09333575'
userid = "1393354621"
aycauserid= "2071273069"
useridtestacc = "48804734072"
aycausername = "aycaa_ozturk"
cached_settings = ""

test = farewells.Farewells()
print(test.randomFarewell())

# with open('data/userdata.json', 'w') as file:
#     username = "tomtestaccount1234"
#     password = "09333575"
#     login_data = {'username' : username, 'password' : password}
#     json.dump(login_data, file)


login_data = jsonManager.loadUserdata()
password = login_data['password']
user_name = login_data['username']

try:
  cached_settings = jsonManager.loadCachedSession()
  api = Client(user_name, password, settings = cached_settings)
except Exception as e:
  print ("Cached Session File was outdated or not found, create new one...")
  api = Client(user_name, password)
  jsonManager.dumpCachedSession(api.settings)
  print("New File created")

print api



#api = Client(user_name, password)
#with open('data.txt', 'w') as outfile:
#    json.dump(api.settings, outfile)

# with open('data.txt') as json_file:
#     cached_settings = json.load(json_file)
# api = Client(user_name, password, settings = cached_settings)

#input_name = raw_input("Type in your instagram name: ")

input_name = "tamibaer_"
#input_name = "tomtestaccount1234"
input_info = api.username_info(input_name)
input_id = input_info['user']['pk']
input_fullname = input_info['user']['full_name']
input_followerCount = input_info['user']['follower_count']
#friendsIC =input_info['user']['mutual_followers_count']    #Friends In Common
input_isPrivate = input_info['user']['is_private']

if(not input_isPrivate):
    print("Oh i realized you have a public account")

print("Oh hello " + input_fullname)

api.friendships_create(input_id)
#while(not api.friendships_show(input_id)['following']):
#    time.sleep(5)
#    print("Waiting for Acception...")
print("Anfrage Akzeptiert")
if(len(api.user_feed(input_id)['items']) < 1):
     print("There is no post where i could Comment :(")
print( len(api.user_feed(input_id)['items'])) 
latestMediaId = api.user_feed(input_id)['items'][17]['id']
post_info = api.media_info(latestMediaId)
like_count = post_info['items'][0]['like_count']
#api.post_comment(latestMediaId, "test Comment 123")
commentGen = comments.Comments()
print (commentGen.generateComment(api, input_name, latestMediaId))
#commentGen.postComment(api,input_name)
link = str(api.media_permalink(latestMediaId)['permalink'])
beg_search = 'https://www.instagram.com/p/'
beg = link.index(beg_search)+len(beg_search)
end = link.index('/?utm', beg)
shortcode = link[beg : end]


interpretInstaPic(shortcode)


with open('usernamefeed.txt', 'w') as outfile:
    json.dump(api.user_info(input_id), outfile)

with open('postinfo.txt' , 'w') as outfile:
    json.dump(api.media_info(latestMediaId), outfile)



