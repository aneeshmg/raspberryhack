''' Imports '''

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
from picamera import PiCamera
from subprocess import call
import subprocess

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
    return c.storage + getLatestImageId() + ".jpg"

def MailSent():
    print "Mail sent to : " + c.email

''' Initialisation '''

camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
configJson = open('config.json', 'r').read()
c = Config(configJson)

''' Initialisation ends '''

while True:
    i=GPIO.input(11)

    if i==0:
           print "No intruders",i
           GPIO.output(3,0)
           time.sleep(c.frequency)


    elif i==1:
            print "Intruder detected",i
            TakePic()
            SendMail(getLatestImage())
            GPIO.output(3,1)
            time.sleep(c.frequency)

