''' Imports '''

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import json
import os
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
from picamera import PiCamera
from subprocess import call
import subprocess
from SimpleCV import Image

''' Imports done '''

''' Class definitions '''

class Config(object):
    def __init__(self, jsonData):
        self.__dict__ = json.loads(jsonData)


''' Config setup done '''

''' emailer '''

def SendMail(ImageFile):
    call(["mpack", "-s", c.basicSubject, "-d", c.TextMessageFile, ImageFile, c.email])
    ''' For async call
    subprocess.Popen(["mpack", "-s", c.basicSubject, "-d", c.TextMessageFile, ImageFile, c.email])
    '''

''' emailer done '''

def getLatestImageId():
    imgs = os.listdir(c.storage)
    return str(len(imgs))

def TakePic():
    latestIndex = getLatestImageId()
    latestIndex = int(latestIndex)
    latestIndex = latestIndex + 1
    camera.capture(c.storage + str(latestIndex) + ".jpg")

def getLatestImage():
    return str(c.storage) + str(getLatestImageId()) + ".jpg"

def MailSent():
    print "Mail sent to : " + c.email

def CleanUp():
    files = glob.glob(c.storage+"*")
    for f in files:
        os.remove(f)

''' Initialisation '''

camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
time.sleep(2)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
configJson = open('config.json', 'r').read()
c = Config(configJson)

''' Initialisation ends '''

while True:
    i=GPIO.input(11)
    if int(getLatestImageId()) > 5:
        CleanUp()

    if i==0:
        GPIO.output(3,0)
    elif i==1:
        print "Intruder detected"
        TakePic()
        foto = Image(getLatestImage())
        facePresent = foto.findHaarFeatures('face.xml')
        if facePresent:
            for face in facePresent:
                print "Face coordinates : " + str(face.coordinates())
                print "Intruder with face present"
                SendMail(getLatestImage())
        else:
            print "Obstruction not a face"

        time.sleep(c.frequency)

