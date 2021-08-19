import instaloader
import os
from instaloader import Post   
import time

def downloadPicture(shortcode, path):
    
    
    #Clean up the #Pictures Folder
    try:
        files = os.listdir(path)
        for index, file in enumerate(files):
         os.remove(os.path.join(path, file))
    except Exception as e:
        pass
    
    #Download the Pictures
    insta = instaloader.Instaloader()
    try:
        insta.load_session_from_file('tomtestaccount1234')
    except FileNotFoundError as e:
        insta.login('tomtestaccount1234' , '09333575')
    post = Post.from_shortcode(insta.context, shortcode)
    insta.download_post(post , target=path)
    files = os.listdir(path)
    
    #Rename and clean the files in #Pictures folder (delete all JSON and txt files)
    counter = 0
    for index, file in enumerate(files):
        if(str(file).endswith('.json.xz') or str(file).endswith('.txt')):
            os.remove(os.path.join(path,file))
            continue
        os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(counter), '.jpg'])))
        counter += 1


#downloadPicture('CDQvCMAJNZk')
