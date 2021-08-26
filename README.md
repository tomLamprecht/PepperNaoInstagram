# READ ME for the NAO & PEPPER Instagram Bot

**Version ALPHA**
---
![Python 2.7, 3.7](https://img.shields.io/badge/Python-2.7%2C%203.5-3776ab.svg?maxAge=2592000)

This is currently a unstable build of this Instagram bot for Pepper and Nao
---

## Overview

This is a basic programm for the roboters Pepper and Nao. It can like, comment and interpret Instagram posts. Pepper is using his tablet and Nao a laptop to writedown a username. This is meant to be a show performance programm, there are <u><b>no</b></u> methods or classes that are meant to be used outside of this Programm.


[Installation Guide](#install-guide)

[License & Copyright](#license)

---


<a name="install-guide"></a>

## Installation Guide


Following Python versions with matching Libraries have to be installed for the programm in order to work properly.


### Python 2.7
(<u>PIP dropped the support for Python 2 in January 2021, therfore all Libraries for Python 2.7 have to be installed manuelly</u>)

with:\
    &ensp;[naoqi Python SDK](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-2.1.4.13.win32.exe)\
    &ensp;[Private Instagram API for Python](https://github.com/ping/instagram_private_api#install) (<u>The Installation Guide is outdated!</u>)


**After you have installed both Libraries you have to fix a bug in the [Private Instagram API for Python](https://github.com/ping/instagram_private_api).**

Go to your Python27 folder. There you direct to:

` Lib>site-packages>instagram_private_api`

and open the [client.py](https://github.com/ping/instagram_private_api/blob/master/instagram_private_api/client.py) file.

Go to line 540 (in older versions line 521) and surround the line with a try catch block.\
like this:
```
try:
    self.logger.debug('RESPONSE: {0:d} {1!s}'.format(response.code, response_content))
except Exception as e:
        pass
```

**Alternative**

Go to your Python27 folder and direct to:

` Lib>site-packages>instagram_private_api`

replace the `client.py` file with [this file](client.py) 


This prevents the Programm to crash when a non-ascii-letter like 'ä', 'ö' or 'ü' is occurring.
<br>
<br>
### Python 3.7
with:\
    &ensp;deep-translator==1.5.0\
    &ensp;tensorflow==2.4.0\
    &ensp;numpy==1.19.3\
    &ensp;scipy==1.4.1\
    &ensp;opencv-python==4.5.3.56\
    &ensp;pillow==7.0.0\
    &ensp;matplotlib==3.3.2\
    &ensp;h5py==2.10.0\
    &ensp;keras==2.4.3\
    &ensp;imageai=2.1.6

these are all the versions that worked for me. Others may work aswell but i cant promise it.
<br>

#### Type the following statements into your Console to install all needed Python 3 Libraries:

Install Tensorflow
```
pip install tensorflow==2.4.0
```
 *<b>Or</b> Tensorflow GPU if you have NVIDIA GPU with CUDA and cuDNN installed:*
```
pip install tensorflow-gpu==2.4.0
```
Then add all other libraries:
```
pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0 deep-translator==1.5.0
```


---
<a name="license"></a>

## License & copyright

© Tom Lamprecht, FHWS Fakultät Informatik
