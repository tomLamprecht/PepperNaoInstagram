# READ ME for the NAO & PEPPER Instagram Bot

**Version 1.0.0**
---

This is currently a unstable build of this Instagram bot for Pepper and Nao

---

**Install guide**

Following Python versions with matching Libraries have to be installed for the programm in order to work properly.

<b>Python 2.7</b>\
with:\
    &ensp;naoqi Python SDK (https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-2.1.4.13.win32.exe)\
    &ensp;Private Instagram API for Python (https://github.com/ping/instagram_private_api#install The Install Guide is outdated! PIP Install not working anymore)

<u>(PIP dropped the support for Python 2 in January 2021, therfore all Libraries for Python 2.7 have to be installed manuelly)</u>

<b>Python 3.7</b>\
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
    &ensp;imageai=2.1.6\

these are all the versions that worked for me. Others may work aswell but i cant promise it.\

Type the following statements into your Console to install all needed Python 3 Libraries:

pip install tensorflow==2.4.0\
<u>or</u> Tensorflow GPU if you have NVIDIA GPU with CUDA and cuDNN installed:\
    &ensp;pip install tensorflow-gpu==2.4.0\
and all other libs:\
pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0 deep-translator==1.5.0

---

## License & copyright

© Tom Lamprecht, FHWS Fakultät Informatik
