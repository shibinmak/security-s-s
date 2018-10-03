"""

** coded by shibinmak on 3/10/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""

from twilio.rest import Client
import config
from datetime import datetime
timestamp = datetime.now().strftime("%d-%b-%Y | %H:%M:%S").upper()
location = config.Location
admin = config.admin
class WhatsApp:
    @staticmethod
    def sendWhatsApp():
        account_sid = config.whatsappSID
        auth_token = config.whatsappKey
        client = Client(account_sid, auth_token)
        info ="[SECURITY ALERT!]\n Your Kind Attention Please.\n Mr.{}\n [MESSAGE]:An unknown person has been detected in your premises. \n [LOCATION]:{} \n [TIME]: {}.\n [NOTE]:Suspect's Image has been send to your registered email address.\nKINDLY TAKE NECESSARY ACTIONS. ".format(admin,location, timestamp)

        number = 'whatsapp:'+config.whatsappNumber

        message = client.messages.create(
            body=info,
            from_='whatsapp:+14155238886',
            to='whatsapp:+919061455955')

        print(message.status)
        print('[INFO] WHATSAPP MESSAGE SEND!')