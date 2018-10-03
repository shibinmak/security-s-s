"""

** coded by shibinmak on 1/10/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import requests
import json
import config
from datetime import datetime


class SMSAlert:
    @staticmethod
    def SendSMS():
        url = "https://www.fast2sms.com/dev/bulk"
        timestamp = datetime.now().strftime("%d-%b-%Y | %H:%M:%S").upper()
        location = config.Location
        key = config.SMSKey
        destination = config.SMSNumber
        admin = config.admin
        info = "[SECURITY ALERT!]\nYour Kind Attention Please.\nMr.{}\n[MESSAGE]:An unknown person has been detected in your premises.\n[LOCATION]:{}\n[TIME]: {}.\n[NOTE]:Suspect's Image has been send to your registered email address.\n KINDLY TAKE NECESSARY ACTIONS. ".format(
            admin, location, timestamp)
        payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers={}".format(info,destination)
        headers = {
            'authorization': key,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)


        print(response.text)
        print('[INFO] SMS SEND !')
