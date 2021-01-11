#!/usr/bin/python3

import requests
import config
# from __future__ import print_function, division, unicode_literals
#
# from config import twilio_conf
# from twilio.rest import Client
#
# client = None
# if twilio_conf['account_sid'] and twilio_conf['auth_token']:
#     client = Client(twilio_conf['account_sid'], twilio_conf['auth_token'])
#
#
# def send_sms(message):
#     if client:
#         client.api.account.messages.create(
#             to=twilio_conf['tonumber'],
#             from_=twilio_conf['fromnumber'],
#             body=twilio_conf['msgprefix'] + message)


# def send_sms(message):
#     print('--message--',message)
#     payload = f"sender_id=Shanmugapriyan&message={message}&language=english&route=p&numbers=8667508556"
#     response = requests.request("POST", config.sms_url, data=payload, headers=config.headers)
#     print(response.text)

# send_sms("TESTING FAST2SMS")


import smtplib

# =============================================================================
# SET EMAIL LOGIN REQUIREMENTS
# =============================================================================
gmail_user = 'spshanmugapriyan641@gmail.com'
gmail_app_password = ''

# =============================================================================
# SET THE INFO ABOUT THE SAID EMAIL
# =============================================================================
sent_from = gmail_user
sent_to = ['spshanmugapriyan641@gmail.com']
sent_subject = "BTC bot"


# =============================================================================
# SEND EMAIL OR DIE TRYING!!!
# Details: http://www.samlogic.net/articles/smtp-commands-reference.htm
# =============================================================================
def send_email(message):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, message)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
