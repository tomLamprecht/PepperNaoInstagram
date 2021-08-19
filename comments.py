# This Python file uses the following encoding: utf-8

from instagram_private_api import Client, ClientCompatPatch
import random

class Comments:

    def generateComment(self,api, username, mediaID):
        user_info = api.username_info(username)
        post_info = api.media_info(mediaID)
        
        likes = post_info['items'][0]['like_count']
        user_realname = user_info['user']['full_name']
        comment_count = post_info['items'][0]['comment_count']
        if(comment_count == 0):
            return "Erster!"
        return self.__randomComment(user_realname, likes, comment_count)


    def __randomComment(self, name, likes, comment_count):
        liste = [(u" Hey, hübsches Bild ") +name , "Die " + str(likes) + " likes hast du mit dem Bild definitiv verdient!", u'Ich bin programmiert dir zu sagen dass deine Bilder schön sind aber das ist wirklich ein klasse Bild! :o', u'Das Bild ist so heiß ich glaube meine Motoren überhitzen!', u'']
        if (comment_count > 10):
            liste.append(u'Bereits ' + str(comment_count) + u' Kommentare??? Ich wünschte ich hätte soviele Freunde!')
        length = len(liste)
        return liste[random.randint(0 , length-1)]

    def postComment(self, api, username):
        user_info = api.username_info(username)
        mediaID = api.user_feed(user_info['user']['pk'])['items'][0]['id']
        comment = self.generateComment(api, username, mediaID)
        api.post_comment(mediaID, comment)
