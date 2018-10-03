"""

** coded by shibinmak on 1/10/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
admin ='SHIBIN MAK'
parentname = os.getcwd().split('/')[3]
parent = os.path.join(os.getenv('HOME'), parentname)
datafolder = os.path.join(parent, 'data')
EmailUserName = ''
EmailPassword = ''
whatsappKey =''
whatsappSID=''
SMSKey = ""
SMSNumber = 9061455955
whatsappNumber = '+919061455955'
Location = 'PARKING SLOT'
camip = 'http://192.168.1.100:8003/video'
video = os.path.join(datafolder,'cctvparking.mp4')
model = os.path.join(parent, 'model', 'MobileNetSSD_deploy.caffemodel')
prototxt = os.path.join(parent, 'model', 'MobileNetSSD_deploy.prototxt.txt')
classes = os.path.join(parent, 'Alerts', 'classes.json')
