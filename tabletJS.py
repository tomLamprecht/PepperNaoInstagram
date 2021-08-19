#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time

#This GUI is only for Pepper! For Nao GUI look at gui.py

class TabletJS:

    def __init__(self, session):
        self.session = session
        self.nameSet = False

    def runJS(self):
        """
        This example uses the executeJS method.
        To Test ALTabletService, you need to run the script ON the robot.
        """
        # Get the service ALTabletService.
        tabletService = self.session.service("ALTabletService")

        try:
            # Display a local web page located in boot-config/html folder
            # The ip of the robot from the tablet is 198.18.0.1
            tabletService.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")

            time.sleep(3)

            # Javascript script for displaying a prompt
            # ALTabletBinding is a javascript binding inject in the web page displayed on the tablet
            #FROM NOW ON CODE IS IN JAVA SCRIPT
            script = """
                var myWindow = window.open("", "", "width=200, height=10");   // Opens a new window
                myWindow.document.write("<p>Developer: Tom Lamprecht</p><p>2. Semester</p>");      
                myWindow.blur();   
                document.body.style.backgroundColor = "darkOrange";
                var confirmed = false;
                var name = ""
                while(!confirmed){
                    name = prompt("Schreib hier deinen Instagram Namen rein", name);
                    if(name == "null"){
                     var alertMessage = "";
                     for(var i = 0; i < 10005 ; i += 1){
                     alertMessage = alertMessage + "💩";
                     }
                     alert(alertMessage);
                     confirmed = true;
                    }
                    else {
                        if(name.length == 0){
                            confirmed = true;
                        }
                        else
                        {
                            confirmed =  confirm("Bestätige bitte deine Eingabe:\\n" + name);
                        }
                    }
                }
                ALTabletBinding.raiseEvent(name);
            """
            #FROM HERE CODE IS PYTHON AGAIN
            
            # Don't forget to disconnect the signal at the end
            signalID = 0

            # function called when the signal onJSEvent is triggered
            # by the javascript function ALTabletBinding.raiseEvent(name)
            def callback(event):
                print "your name is:", event
                if(event != 'null'):
                    self.nameSet = True
                else:
                    self.nameSet = False

                self.name = event
                promise.setValue(True)


            promise = qi.Promise()

            # attach the callback function to onJSEvent signal
            self.signalID = tabletService.onJSEvent.connect(callback)


            # inject and execute the javascript in the current web page displayed
            tabletService.executeJS(script)

            try:
                promise.future().hasValue(300000) #nach 5 Minuten beendet das tablet die Application. Bei bedarf jederzeit verlängerbar
            except RuntimeError:
                self.closeJS()
                raise RuntimeError('Timeout: no signal triggered')

        except Exception, e:
            print "Error was: ", e

        self.closeJS()

    def closeJS(self):
        tabletService = self.session.service("ALTabletService")
        # Hide the web view
        tabletService.hideWebview()
        # disconnect the signal
        tabletService.onJSEvent.disconnect(self.signalID)

#session = qi.Session()
#session.connect("10.30.4.8:9559")
#test = TabletJS(session)
#test.runJS()

