''' Imports '''

from picamera import PiCamera
from time import sleep
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import call

''' Imports done '''
''' Class definitions '''

class Config(object):
    def __init__(self, jsonData):
        self.__dict__ = json.loads(jsonData)


configJson = open('config.json', 'r').read()

c = Config(configJson)

''' Config setup done '''

''' emailer '''

def SendMail(ImageFile):
    call(["mpack", "-s", c.basicSubject, "-d", c.TextMessageFile, ImageFile, c.email])

''' emailer done '''

def getLatestImageId():
    imgs = os.listdir(c.storage)
    return str(len(imgs))

def TakePic():
    latestIndex = getLatestImageId()
    latestIndex = int(latestIndex)
    latestIndex = latestIndex + 1
    camera = PiCamera()
    camera.capture(c.storage + str(latestIndex) + ".jpg")

def getLatestImage():
    return c.storage + getLatestImageId() + ".jpg"

'''SendMail(c.storage + getLatestImage())'''
TakePic()
SendMail(getLatestImage())



"""

camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()

"""
