#!/usr/bin/env python

import os

import requests
import json
import datetime
import time

import smtplib

# FUNCTIONS
def pwm(pin, angle):
   angle = checkmax(angle)
      print "servo[" + str(pin) + "][" + str(angle) + "]"
      cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/servoblaster"
      os.system(cmd)

def checkmax(angle): #PWM can only handle 249 units, so we're simply cutting the hex values 250-255 down to 249
   if angle > 249:
      angle = 249
   return angle

def setcolor(hex):
   pwm(5, int(hex[1:3],16))
   pwm(2, int(hex[3:5],16))
   pwm(0, int(hex[5:7],16))

# Define a Thank You Email
def send_email():
   SMTP_SERVER = 'smtp.gmail.com'
   SMTP_PORT = 587

   sender = ''
   password = ''
   recipient = data[0]['email_address']
   subject = 'Color My Desk: Thank you!'
   body = 'Hey '+data[0]['name']+",<br /><br />"+"Thanks for setting my desk color to <span style='color:"+data[0]['color']+"'>" + data[0]['color'] + "</span> today! <br /><br />"+"You wrote: "+data[0]['details']+"<br /><br />"+"Will Wnekowicz"

   headers = ["From: " + sender,
              "Subject: " + subject,
              "To: " + recipient,
              "MIME-Version: 1.0",
              "Content-Type: text/html"]
   headers = "\r\n".join(headers)

   session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

   session.ehlo()
   session.starttls()
   session.ehlo
   session.login(sender, password)

   session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
   session.quit()

# Getting the JSON Feed
os.environ['TZ'] = 'America/New_York'
time.tzset()
r = requests.get('http://colormydesk.com/full_calendar/events/feed?start='+str(datetime.date.today())+'&api_secret=thesecret')
data = r.json()

# Setting the Color of the Strip
if data:
   setcolor(data[0]['color'])
   send_email()
else:
   setcolor("#7733F0") # default color if no color is scheduled, aka no one loves me.
