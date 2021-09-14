# This Python file uses the following encoding: utf-8

#Falls auf die Frage ob man Insta hat nicht mit Ja oder Nein antwortet kann es dazu kommen das der Roboter
#nicht mehr aus dem Dialog rauskommen kann. In solchen Fällen auf keinen Fall das Programm terminieren sonder
#mit dem Sprachbefehl "EXIT" den Roboter zum terminieren zwingen!

import qi
import time
import thread as th
from naoqi import ALProxy
import dances as dan

class Dialog:

    def  __init__(self, session, robot_ip):
        self.robot_ip = robot_ip
        self.done = False
        self.session = session
        self.ALDialog = session.service("ALDialog")
        self.memory = session.service("ALMemory")
        self.motion = session.service("ALMotion")
        self.dances = dan.Dances()

        if "HoldHandsAnswered" in self.memory.getEventList():
            pass
        else:
            self.memory.declareEvent("HoldHandsAnswered")

        if "NyanCat" in self.memory.getEventList():
            pass
        else:  
            self.memory.declareEvent("NyanCat")

        if "HasInstaAnswered" in self.memory.getEventList():
            pass
        else:
            self.memory.declareEvent("HasInstaAnswered")


    def hands_callback(self, value):
        self.motion.openHand("RHand")
        self.motion.openHand("LHand")
        time.sleep(1)
        self.motion.closeHand("LHand")
        self.motion.closeHand("RHand")

    
    def hasInstaAnswered_callback(self, hasInsta):
        time.sleep(1)
        if(hasInsta == 'True'):
          #  self.session.service("ALAnimatedSpeech").say("Alles klar")
            self.stopTopic()
            self.done = True
        else:
          #  self.session.service("ALAnimatedSpeech").say("Tschüssi")
            self.stopTopic()
            th.interrupt_main()
            quit()

    def on_userinput(self, value):
        print(value)

    def nyancat_callback(self, value):
        robotPosture = self.session.service("ALRobotPosture")
        tts = self.session.service("ALTextToSpeech")

        robotPosture.goToPosture("Sit",70)
        tts.say("LOS GEHTS!")
        aup = ALProxy("ALAudioPlayer", self.robot_ip, 9559)
        aup.post.playFile("/data/home/nao/music/nyan_cat.mp3")
        self.dances.dance2(self.session)
        time.sleep(1)
        aup.stopAll()
        robotPosture.goToPosture("Stand", 70)
        aup.unloadAllFiles()

    def on_answered(self, value):
        #OUTDATED
        print(value)
        if(str(value).__contains__("Bis dann")):
            self.stopTopic()
            self.done = True
            th.interrupt_main()
            quit()
        if(str(value).__contains__("alles klar")):
            self.stopTopic()
            self.done = True
            

    def start(self):
        #add the callback method to the Robot Answered Event
        subscriber = self.memory.subscriber("Dialog/Answered")
        subscriber.signal.connect(self.on_answered)

        self.session.service("ALAnimatedSpeech").say("\\rspd=95\\Programm gestartet.\\pau=500\\ Bitte antworten Sie mit ein bis zwei wörtern, da meine Spracherkennung noch nicht sehr fortgeschritten ist.\\pau=500\\ Bestätigen Sie dies bitte indem Sie . OK. sagen.")


        #set Lanuage
        self.ALDialog.setLanguage("German")

        self.topic_content_1 = ('topic: ~myTopic()\n'
                    'language: ged\n' #"German" for Nao "ged" for pepper
                    'concept:(farben) [rot gelb blau gruen lila orange schwarz weiss grau tuerkis Rosa Violett Braun Silber Gold]\n'
                    'proposal: Hast du Ins ta gram?\n'
                        'u1: ([ja yes jo jap]) alles klar ^call(ALMemory.raiseEvent("HasInstaAnswered", True))\n'
                        'u1: ([nein nö ne nope]) okay schade. Bis dann!^call(ALMemory.raiseEvent("HasInstaAnswered", False))\n'
                    'u: ([Pepper Hallo Hey Hi "Guten Morgen" Abend Tag "Grueß Gott" Servus Sers OK okay]) Hallo Mensch. Ich bin der Roboter '+self.session.service("ALSystem").robotName()+'. Wie geht es dir?\n'
                    'u1: ([gut "sehr gut" Gut gud gudh guth kut mut jut super klasse grandios fantastisch]) das freut mich. Was ist deine Lieblingsfarbe?\n'
                            'u2: (_~farben) ["$1==gelb gelb ist eine schöne Farbe. Meine Lieblingsfarbe ist auch Gelb. \\pau=1000\\ ^nextProposal" "$1 ist eine schoene Farbe. Meine Lieblingsfarbe ist Gelb. \\pau=1000\\ ^nextProposal"]\n'
                        'u1: ([schlecht "nicht so gut" naja "geht schon"]) Oh das ist schade. Vielleicht solltest du mit einem anderen Menschen darueber reden, ich bin nicht so gut mit Gefuehlen.\\pau = 1000\\ Was ist deine lieblingsfarbe?\n'
                            'u2: (_~farben) ["$1==gelb gelb ist eine schöne Farbe. Meine Lieblingsfarbe ist auch Gelb. \\pau=1000\\ ^nextProposal" "$1 ist eine schoene Farbe. Meine Lieblingsfarbe ist Gelb. \\pau=1000\\ ^nextProposal"]\n'
                    'u: (["Wie geht es dir" "Wie gehts" "Was geht" "Wie laeufts" "was los"]) Gut und selbst?\n'
                        'u1: ([auch gut gud gudh guth kut mut genauso super klasse grandios fantastisch]) das freut mich.\\pau = 1000\\ Was ist deine Lieblingsfarbe?\n'
                            'u2: (_~farben) ["$1==gelb gelb ist eine schöne Farbe. Meine Lieblingsfarbe ist auch Gelb. \\pau=1000\\ ^nextProposal" "$1 ist eine schoene Farbe. Meine Lieblingsfarbe ist Gelb. \\pau=1000\\ ^nextProposal"]\n'
                        'u1: ([schlecht "nicht so gut" naja "geht schon"]) Oh das ist schade. Vielleicht solltest du mit einem anderen Menschen darueber reden, ich bin nicht so gut mit Gefuehlen.\\pau = 1000\\ Was ist deine Lieblingsfarbe?\n'
                            'u2: (_~farben) ["$1==gelb gelb ist eine schöne Farbe. Meine Lieblingsfarbe ist auch Gelb. \\pau=1000\\ ^nextProposal" "$1 ist eine schoene Farbe. Meine Lieblingsfarbe ist Gelb. \\pau=1000\\ ^nextProposal"]\n'

                    'u: ([e:FrontTactilTouched e:MiddleTactilTouched e:RearTactilTouched]) Sach ma ich fass doch auch nicht "deinen" Kopf an oder?!\n'
                    'u: ([e:LeftBumperPressed e:RightBumperPressed e:BackBumperPressed]) Autsch! Was soll das denn?!\n'
                    'u: ([e:HandLeftLeftTouched e:HandRightRightTouched]) Willst du Haendchen halten?\n'
                        'u1: ([ja yes jo jap]) okay, gib mir deine Hand.^call(ALMemory.raiseEvent("HoldHandsAnswered",0))\n'
                        'u1: ([nein ne noe]) dann halt nicht.\n'
                    'u: (exit) Tschuess. ^call(ALMemory.raiseEvent("HasInstaAnswered", False))\n'
                    'u: (neien kät) ^call(ALMemory.raiseEvent("NyanCat", True))\n')
                   # 'u:(e:Dialog/NotUnderstood) Es tut mir leid, das hab ich nicht verstanden. Kannst du es vielleicht nocheinmal für mich wiederholen? \n')
        
        self.memory = self.session.service("ALMemory")
        # Connect the event callback.
        #self.subscriber = self.memory.subscriber("Dialog/Answered")
        #self.subscriber.signal.connect(self.on_answered)

        #self.subscriber2 = self.memory.subscriber("Dialog/LastInput")
        #self.subscriber2.signal.connect(self.on_userinput)

        self.subscriber3 = self.memory.subscriber("HoldHandsAnswered")
        self.subscriber3.signal.connect(self.hands_callback)

        self.subscriber4 = self.memory.subscriber("HasInstaAnswered")
        self.subscriber4.signal.connect(self.hasInstaAnswered_callback)

        self.subscriber5 = self.memory.subscriber("NyanCat")
        self.subscriber5.signal.connect(self.nyancat_callback)

        
        # Loading the topics directly as text strings
        self.topic_name_1 = self.ALDialog.loadTopicContent(self.topic_content_1)
        self.ALDialog.activateTopic(self.topic_name_1)
        self.ALDialog.subscribe('myTopic')

    def stopTopic(self):
         self.ALDialog.unsubscribe('myTopic')

         self.ALDialog.deactivateTopic(self.topic_name_1)
         self.ALDialog.unloadTopic(self.topic_name_1)

         print("TOPIC STOPPED")



#session = qi.Session()
#session.connect("194.95.223.91:9559")
#session.service("ALRobotPosture").goToPosture("StandInit",10)
#dia = Dialog(session, "194.95.223.91")
#dia.start()
#raw_input("as")
#dia.stopTopic()

#while(not dia.done):
#    pass
