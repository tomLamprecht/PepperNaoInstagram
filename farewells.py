import random

class Farewells:
    liste = ["See you later, aligator", "bye bye, butter fly" , "See you in a while, crocodile" , "See you soon, Racoon", "Time to go, buffalo", "Take care, teddy bearr", "Say goodbye, pumpkin pie" ]
    

    def randomFarewell(self):
        size = len(self.liste)
        index = random.randint(0, size-1)
        return self.liste[index]