# coding=utf-8
# This Python file uses the following encoding: utf-8
# LANG=en_US.UTF-8


from instagram_private_api import Client, ClientCompatPatch
import qi
from naoqi import ALProxy
import time
import json
import farewells
import gui
from threading import Thread
import dialog as dia
import os
import comments
import unicodedata
import jsonManager

#-----------------------------------------MOVEMENT FUNCTIONS------------------------------------------------------------





#-------------------------------------------HERE BEGINS THE REAL CODE--------------------------------------------------

def interpretInstaPic(shortcode):
    os.system('py -3.7 imageRecognition.py --shortcode '+shortcode)

    results = jsonManager.loadImageRecognitionResults()

    print(results[1]['prediction_translated'] + " " + str(results[1]['probability']) + '%')
    print(results[0]['prediction_translated'] + " " + str(results[0]['probability']) + '%')

    return results[0]

def main(args):

  if args.username is None:
    login_data = jsonManager.loadUserdata()
    user_name = login_data['username']
    password = login_data['password']
  else:
    user_name = args.username
    password = args.password
  
  userid = "1393354621"
  aycauserid= "2071273069"
  useridtestacc = "48804734072"
  aycausername = "aycaa_ozturk"

  # Get the instagram api client, preferable by cached Session
  try:
    cached_settings = jsonManager.loadCachedSession()
    api = Client(user_name, password, settings = cached_settings)
  except Exception as e:
    print ("Cached Session File was outdated or not found, create new one...")
    api = Client(user_name, password)
    jsonManager.dumpCachedSession(api.settings)
    print("New File created")

  goodbyes = farewells.Farewells()

  session = qi.Session()
  #robot_ip = "192.168.178.93"
  #robot_ip = "10.30.4.31"
  #robot_ip = "194.95.223.91"
  robot_ip = args.ip
  session.connect(robot_ip+":9559")
  animatedSpeech = session.service("ALAnimatedSpeech")
  postureService = session.service("ALRobotPosture")
  tts = session.service("ALTextToSpeech")
  speechReco = session.service("ALSpeechRecognition")
  memory = session.service("ALMemory")
  dialog = dia.Dialog(session, robot_ip)
  aup = ALProxy("ALAudioPlayer", robot_ip, 9559)
  asr = ALProxy("ALSpeechRecognition", robot_ip, 9559)

  tts.setLanguage("German")

  aup.stopAll()
  aup.unloadAllFiles()
  postureService.goToPosture("Stand", 70)
  inputGUI = gui.GUIThread()
  t = Thread(target = inputGUI.run)
  t.start()
  tts.setParameter("speed", 70)




  ##HERE THE DIALOG BOX

  dialog.start()

  while(not dialog.done):
    pass

    # #dialog.stopTopic()

  #animatedSpeech.say("Das freut mich zu hoeren. Wenn du willst, dass ich dir ein Kommentar auf ihns ta gram da lasse, schreib deinen Namen auf den Laptop")


  time.sleep(2)
  correctInput = False
  while(not correctInput):
    while(not inputGUI.submitted):
      pass
    

    input_name = inputGUI.userInput
    print(input_name)
    #input_name = "tom_15_01"
    try:
      input_info = api.username_info(input_name)
      correctInput = True
    except Exception, e:
      if(len(input_name) == 0):
        animatedSpeech.say("\\rspd=90\\Schreibe bitte zuerst deinen Namen in die Box hinein.\\rspd=100\\\\pau=500\\ Versuch es nochmal!")
      else:
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

  animatedSpeech.say("Dein Ins ta gram name ist: " + input_name + ".")


  input_fullname = unicodedata.normalize('NFC', input_fullname)


  try:
    animatedSpeech.say("Ich glaube dein tatsaechlicher Name ist: " +unicode(input_fullname) + ".")
  except Exception as e:
    #Probably couldnt display weird characters
    print(e)
    pass
  time.sleep(1)
  tts.setParameter("speed", 90)
  if(friendsIC == 0):
      animatedSpeech.say("Oh, ich kenne leider niemanden von deinen Freunden.\\pau=500\\ Vielleicht willst du mich Ihnen ja spaeter vorstellen?\\pau=800\\ nichts desto trotz:")
  else:
      animatedSpeech.say("Hey! ich kenne bereits " + str(friendsIC) + " von deinen Freunden!")
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
          try:
            friend_info = api.username_info(friend_username)
          except:
            continue
          friend_fullname = friend_info['user']['full_name']
          if( ((friendsIC - i) == 1 or (maxShowable - i) == 1) and friendsIC != 1):
              if(maxShowable != 1):
                  friend_fullname = filler+ friend_fullname
          friend_fullname = unicodedata.normalize('NFC', friend_fullname)
          try:
            animatedSpeech.say(unicode(friend_fullname))
          except:
            pass
          time.sleep(0.5)
      time.sleep(1)

  tts.setParameter("speed", 90)
  tts.say("Ich lasse dir einen netten Kommentar dar und Folge dir. Wie es sich nunmal fuer einen guten Roboter gehoert")
  time.sleep(1)
  if(not input_isPrivate):
      animatedSpeech.say("Oh. Du hast einen oeffentlichen Account. \\pau=1000\\  Vielleicht solltest du etwas mehr auf deine Sicherheit im Internet achten!")
      time.sleep(1)
      tts.say("nichts desto trotz...")
      api.friendships_create(input_id)
  else:
    animatedSpeech.say("Zuerst musst du jedoch meine Anfrage bestaetigen.")
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
            aup.unloadAllFiles()
            animatedSpeech.say("\\vol=100\\\\vct=65\\ Wie Kannst du nur?!")
            time.sleep(2)
            animatedSpeech.say("\\vct= 70\\ Mein Leben hat keinene Sinn mehr!")
            postureService.goToPosture("LyingBelly", 70)
            tts.say("\\vol=100\\\\vct=70\\\\rspd=80\\ Lass mich alleine!")
            inputGUI.readyToDestroy = True
            quit()
    first = False
      
  aup.stopAll()
  aup.unloadAllFiles()
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

    
  #Post Comment
  commentGen = comments.Comments()
  commentGen.postComment(api, input_name)
  api.post_like(latestMediaId)

  #api.post_comment(latestMediaId, "Hello " + input_fullname + "This Is Nao. Beep Boop!")
  animatedSpeech.say("Ich hab dir einen netten Kommentar hinterlassen. Ich hoffe er gefaellt dir!")
  time.sleep(1)
  animatedSpeech.say("Zum Schluss lass mich noch deine Abonennten anzahl anschauen.")
  time.sleep(0.5)
  if(input_follower_count < 100):
      animatedSpeech.say("Oh, du hast unter 100 Abonennten.\\pau=500\\ Immerhin hast du jetzt einen mehr!")
  else:
      number = int(input_follower_count/100) * 100
      animatedSpeech.say("WAS?, du hast ueber " + str(number) + " Abonennten? Das ist sehr beeindruckend!\\pau=800\\ Nichts desto trotz: ")
      


  animatedSpeech.say("Moechtest du vielleicht noch ein kleines Spiel spielen?")

  vocabulary = ["ja", "nein"]
  asr.pause(True)
  asr.setVocabulary(vocabulary, True)
  asr.pause(False)

  class Callback:

    def __init__(self):
      self.answered = False

    def on_answered(self,value):
      self.answered = True
      if(str(value).__contains__("ja")):
        self.wantsToPlay = True
      else:
        self.wantsToPlay = False

  subscriber = memory.subscriber("WordRecognized")
  callback = Callback()
  subscriber.signal.connect(callback.on_answered)
  asr.subscribe("ImageReco_Fragen")
  while(not callback.answered):
    pass
  asr.unsubscribe("ImageReco_Fragen")


  if(callback.wantsToPlay):
    animatedSpeech.say("Okay, schau auf dein neustes Ins ta gram Bild. \\pau=500\\ Ich versuche herauszufinden was auf den Bild zu sehen ist.")
    animatedSpeech.say("Dafuer werde ich aber ein bisschen Zeit brauchen also warte bitte kurz.")
    aup.post.playFile("/data/home/nao/music/music.mp3")
    link = str(api.media_permalink(latestMediaId)['permalink'])
    beg_search = 'https://www.instagram.com/p/'
    beg = link.index(beg_search)+len(beg_search)
    end = link.index('/?utm', beg)
    shortcode = link[beg : end]
    guess = interpretInstaPic(shortcode)
    aup.stopAll()
    aup.unloadAllFiles()
    if(guess['probability'] >= 99):
      animatedSpeech.say("Oh da bin ich mir recht sicher!")
    else:
      animatedSpeech.say("Das war echt nicht leicht. Aber")
    animatedSpeech.say("Ich glaube auf dem Bild befindet sich: \\pau=200\\" + guess['prediction_translated'])
    time.sleep(2)
    animatedSpeech.say("Nichts desto trotz: ")
  else:
    animatedSpeech.say("Okay Schade. ")

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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, required=True, help = "ip-adress of the robot")
    parser.add_argument("--username", type=str, required=False, help = "Username of the Instagram account that the robot will use to like and comment.")
    parser.add_argument("--password", type=str, required=False, help="Password of the matching username")
    args = parser.parse_args()
    main(args)