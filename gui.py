from Tkinter import *
import usernameChecker
from threading import Thread
import time
import thread as th

#This GUI is ONLY for the NAO Roboter!
# Pepper is using his Tablet instead!

colorCodeGreen = "#00ff00"
colorCodeOrange = "#FF5501"
colorCodeRed = "#ff0000"


class GUIThread:
 
    checker = usernameChecker.Checker()
    userInput = ""
    textentry = ""
    window = ()
    readyToDestroy = False           #This attribute should be used to destroy the GUI outside of its own class
    submitted = False
    threads = []

    def resetColor(self):
        self.textentry.config(fg = "black")


    def changeColorOfText(self, color):
        self.textentry.config(fg = color)


    def exitClick(self):
        self.readyToDestroy = True

    def submitEnter(self,event):
        self.submit()

    def submit(self):
        entered_text = self.textentry.get()
        self.userInput = entered_text
        self.submitted = True
        self.textentry.delete(0 , 'end')


    def check(self, sv):
        length = len(self.threads)
        if(length > 1):
            self.threads[length-2].join() #always wait on the Thread before

        if(self.checker.checkUsername(str(sv.get()))):
            self.changeColorOfText(colorCodeGreen)
        else:
            self.changeColorOfText(colorCodeRed)

    def callback(self, sv):
        removeList = []
        for t in self.threads:
            if(not t.isAlive()):
                removeList.append(t)

        for t in removeList:
            self.threads.remove(t)

      #  if(len(self.threads) > 100):    # It Once crashed  cause to many Threads were opend. Therefore this 
      #      for t in self.threads:     # piece of code just waits for all Threads if there were created more than 100
      #          t.join()

        
        self.resetColor()
        t = Thread(target= self.check, args=(sv,))
        self.threads.append(t)
        t.start()


    def run(self):
        self.window = Tk()
        self.window.config(background = "white")

        #background
        background_image= PhotoImage(file='naoBild.gif')
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Textbox
        self.textbox = Label(self.window, text="Write your Instagram Name here:", bg="white", fg=colorCodeOrange, font = "none 24 bold")
        self.textbox.grid(row=0, column=0,sticky=W)

        #Entrybox
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
        self.textentry = Entry(self.window,textvariable=sv, width = 20, bg="gray89",fg = "black", font ="none 24 bold")
        self.textentry.grid(row=1,column=0,sticky=W)
        self.textentry.focus()

        #Submit Button
        self.submitButton = Button(self.window,text="SUBMIT",width=10,font=50,fg = colorCodeOrange, activeforeground = colorCodeOrange ,command=self.submit)
        self.submitButton.grid(row=2,column=0,sticky=W)

        #Exit Button
        Button(self.window,text="EXIT", font= "none 15 bold", bg = "gray75", command=self.exitClick).place(relx=0.95, rely=0, relwidth=0.05, relheight=0.05)

        #Submit Button on Enter Key
        self.window.bind('<Return>', self.submitEnter)

        self.window.attributes("-fullscreen", True)

        self.input_completed = False
        #update loop
        while True:
          try:

            try:
                if(self.input_completed):
                    self.textentry.destroy()
                    self.textbox.config(text= 'Nutzername akzeptiert!')
                    self.submitButton.destroy()
            except Exception as e:
                pass

            self.window.update_idletasks()
            self.window.update()
            
          except Exception, e:
              print(e)
              break #The window got probably Destroyed and therefore cant be updated anymore, Instead of Throwing an Exception just end the run method at this point
          if (self.readyToDestroy):
              self.window.destroy()
              break
        
        th.interrupt_main()      # This Throws a KeyboardInterrupt at the Main Thread, which results in the whole Programm
                                 # closing. The Error Message in the console can be ignored and has no more meaning than that the
                                 # Programm got closed
        

#test = GUIThread()
#test.run()



