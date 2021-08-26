# This Python file uses the following encoding: utf-8

#WICHTIG: Dialoge und GUI Einheiten immer über den Roboter beenden und niemals einfach das Programm terminieren
# ansonten werden Behaviors nicht richtig geschlossen!

from instagram_private_api import Client, ClientCompatPatch
import qi
from naoqi import ALProxy
import time
import json
import farewells
import gui
from threading import Thread
import dialog as dia
import tabletJS as tjs
import os
import comments

#-----------------------------------------MOVEMENT FUNCTIONS------------------------------------------------------------

#Not done for Pepper yet
def moveFunction2(session):
  pass


#-------------------------------------------HERE BEGINS THE REAL CODE--------------------------------------------------

def interpretInstaPic(shortcode):
    os.system('py -3.7 imageRecognition.py --shortcode '+shortcode)

    with open("imageRecognitionData.json") as file:
        results = json.load(file)

    print(results[1]['prediction_translated'] + " " + str(results[1]['probability']) + '%')
    print(results[0]['prediction_translated'] + " " + str(results[0]['probability']) + '%')


user_name = 'tomtestaccount1234'
password = '09333575'
userid = "1393354621"
aycauserid= "2071273069"
useridtestacc = "48804734072"
aycausername = "aycaa_ozturk"


try:
  with open('data.txt') as json_file:
      cached_settings = json.load(json_file)
  api = Client(user_name, password, settings = cached_settings)
except Exception as e:
  print("Cached Settings File was outdated, create new one...")
  api = Client(user_name, password)
  with open('data.txt', 'w') as outfile:
      json.dump(api.settings, outfile)
  print("New File created")

goodbyes = farewells.Farewells()

session = qi.Session()
robotIP = "10.30.4.8"
session.connect(robotIP+ ":9559")
animatedSpeech = session.service("ALAnimatedSpeech")
postureService = session.service("ALRobotPosture")
tts = session.service("ALTextToSpeech")
dialog = dia.Dialog(session, robotIP)
tabletJS = tjs.TabletJS(session)
aup = ALProxy("ALAudioPlayer", robotIP , 9559)

tts.setLanguage("German")

aup.stopAll()
postureService.goToPosture("Stand", 70)
inputGUI = gui.GUIThread()
#t = Thread(target = inputGUI.run)
#t.start()
tts.setParameter("speed", 120)

##HERE THE DIALOG BOX
dialog.start()

while(not dialog.done):
  pass


animatedSpeech.say("Das freut mich zu hoeren. Wenn du willst, dass ich dir ein Kommentar auf ihns ta gram da lasse, schreib deinen Namen auf meine Brust")


moveFunction2(session)
time.sleep(2)
correctInput = False
while(not correctInput):
  #This is a blocking Method
  tabletJS.runJS() 
  input_name = tabletJS.name
  #input_name = "tom_15_01"

  #Falls des Tablet mal wieder nicht funktionieren sollte: (Oben muss der  Thread kommentar auch wieder eingefügt werden)
  '''
    while(not inputGUI.submitted):
      pass
    

    input_name = inputGUI.userInput
  '''

  if(not tabletJS.nameSet):
    animatedSpeech.say("Nagut, vielleicht wann anders? Auf Wiedersehen!")
    quit()

  if(len(input_name) == 0):
    animatedSpeech.say("Schreibe bitte zuerst deinen Namen in die Box hinein.\\rspd=100\\\\pau=500\\ Versuch es nochmal!")
    inputGUI.submitted = False
  else:
    try:
      input_info = api.username_info(input_name)
      correctInput = True
    except Exception, e:
      animatedSpeech.say("Oh, anscheinend kann ich dich nicht auf Ins ta gram finden. Willst du es nochmal versuchen?")
  inputGUI.submitted = False
inputGUI.input_completed = True
input_id = input_info['user']['pk']
input_fullname = input_info['user']['full_name']
input_isPrivate = input_info['user']['is_private']
input_follower_count = input_info['user']['follower_count']
try:
  friendsIC =input_info['user']['mutual_followers_count'] 
except Exception, e:
  animatedSpeech.say("Sehr lustig.\\pau=500\\ Aber ich kann mir nicht selbst auf Ins ta gram folgen!\\pau=800\\ Nagut, wenn das so, ist:")
  tts.setLanguage("English")
  animatedSpeech.say(goodbyes.randomFarewell())
  inputGUI.readyToDestroy = True
  quit()

input_fullname = unicodedata.normalize('NFC', input_fullname)

animatedSpeech.say("Dein Ins ta gram name ist: " + input_name + ".")
try:
  animatedSpeech.say("Ich glaube dein tatsaechlicher Name ist: " +unicode(input_fullname) + ".")
except Exception as e:
  #Probably couldnt display weird characters
  print(e)
  pass
time.sleep(1)

if(friendsIC == 0):
    animatedSpeech.say("Oh, ich kenne leider niemanden von deinen Freunden.\\pau=500\\ Vielleicht willst du mich Ihnen ja spaeter vorstellen?\\pau=800\\ nichts desto trotz:")
else:
    animatedSpeech.say("Ich kenne bereits " + str(friendsIC) + " von deinen Freunden!")
    time.sleep(0.5)
    maxShowable = 3                                             #Amount of Friends that will be shown at max | Max cant be higher than 3!!!
    filler = "und "
    if (friendsIC > maxShowable):
        tts.say("Zum Beispiel: ")
        filler = "oder "
    for i in range(friendsIC):
        if i >= maxShowable:
           break
        friend_username = input_info['user']['profile_context_links_with_user_ids'][i]['username']
        friend_info = api.username_info(friend_username)
        friend_fullname = friend_info['user']['full_name']
        if( ((friendsIC - i) == 1 or (maxShowable - i) == 1) and friendsIC != 1):
            if(maxShowable != 1):
                friend_fullname = filler+ friend_fullname
        animatedSpeech.say(friend_fullname)
        time.sleep(0.5)
    time.sleep(1)


tts.say("Ich lasse dir einen netten Kommentar dar und Folge dir. Wie es sich nunmal fuer einen guten Roboter gehoert")
time.sleep(1)
if(not input_isPrivate):
    animatedSpeech.say("Oh. Du hast einen oeffentlichen Account. \\pau=1000\\  Vielleicht solltest du etwas mehr auf deine Sicherheit im Internet achten!")
    time.sleep(1)
    tts.say("nichts desto trotz...")
    api.friendships_create(input_id)
else:
  animatedSpeech.say("Zuerst musst du jedoch meine Anfrage bestaetigen, " + input_fullname)
  api.friendships_create(input_id)
  aup.post.playFile("/data/home/nao/music/music.mp3")
  done = False
  first = True
  while(not done):
   if(not first):
      animatedSpeech.say("Ich warte...")
   for i in range(16):
      time.sleep(0.5)
      if(not api.friendships_show(input_id)['outgoing_request']):
         if(api.friendships_show(input_id)['following']):
            done = True
            break
         else:
           aup.stopAll()
           animatedSpeech.say("\\vol=100\\\\vct=65\\ Wie Kannst du nur?!")
           time.sleep(2)
           animatedSpeech.say("\\vct= 70\\ Mein Leben hat keinene Sinn mehr!")
           postureService.goToPosture("LyingBelly", 70)
           tts.say("\\vol=100\\\\vct=70\\\\rspd=80\\ Lass mich alleine!")
           inputGUI.readyToDestroy = True
           quit()
   first = False
    
aup.stopAll()
tts.say("\\style=joyful\\ Ich folge dir jetzt!")
tts.setLanguage("English")
animatedSpeech.say("\\style=joyful\\ yea")
tts.setLanguage("German")




latestMediaId = 0
try:
  latestMediaId = api.user_feed(input_id)['items'][0]['id']
except Exception, e:
  time.sleep(2)
  animatedSpeech.say("Oh es tut mir Leid.\\pau=500\\ Aber damit ich dir einen Kommentar schreiben kann, musst du zunaechst ein Bild von dir hochladen.")
  animatedSpeech.say("Vielleicht willst du ja aber spaeter wieder zurueck kommen?")
  time.sleep(0.5)
  tts.setLanguage("English")
  animatedSpeech.say(goodbyes.randomFarewell())
  inputGUI.readyToDestroy = True
  quit()

#Like all posts
def likeAllPosts():
  allMediaIDs = []
  user_feed = api.user_feed(input_id)
  counter = 0
  while(True):
     try:
          allMediaIDs.append(user_feed['items'][counter]['id'])
          counter += 1
     except:
          break

  for mediaID in allMediaIDs:
      print("LIKED")
      api.post_like(mediaID)

th = Thread(target = likeAllPosts)
th.start()

  
  
commentGen = comments.Comments()
commentGen.postComment(api, input_name)
api.post_like(latestMediaId)

animatedSpeech.say("Ich hab dir einen netten Kommentar hinterlassen. Ich hoffe er gefaellt dir!")
time.sleep(1)
animatedSpeech.say("Zum Schluss lass mich noch deine Abonennten anzahl anschauen.")
time.sleep(0.5)
if(input_follower_count < 100):
    animatedSpeech.say("Oh, du hast unter 100 Abonennten.\\pau=500\\ Immerhin hast du jetzt einen mehr!")
else:
    number = int(input_follower_count/100) * 100
    animatedSpeech.say("WAS?, du hast ueber " + str(number) + " Abonennten? Das ist sehr beeindruckend!\\pau=800\\ Nichts desto trotz: ")
    

tts.setLanguage("English")
animatedSpeech.say(goodbyes.randomFarewell())
inputGUI.readyToDestroy = True



#api.post_comment("2403725229450814435_1393354621", "this is a Computer Generated Comment by a Bot. Beep Boop.")
#followers = api.user_followers(userid ,api.generate_uuid())
#counter = 0
#for element in followers["users"]:
 #   print(element["username"])
  #  counter = counter +1
#print(str(counter))
