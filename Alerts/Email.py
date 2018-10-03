"""

** coded by shibinmak on 30/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""

import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import config


class EmailAlert:

    @staticmethod
    def SendEmail(image=None):
        from_address = config.EmailUserName
        username = from_address
        password = config.EmailPassword
        to_address = (Address(display_name='Shibin mak', username='shibinmak23', domain='gmail.com'),
                      Address(display_name='Shibin mak', username='23makjr', domain='gmail.com'))
        message = "An unknown person has been detected in your premises."
        msg = EmailMessage()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = 'SECURITY ALERT'
        msg.set_content(message)
        timestamp = datetime.now().strftime("%d-%b-%Y | %H:%M:%S").upper()
        location = config.Location
        note1 = 'KINDLY TAKE NECESSARY ACTIONS.'
        note2 = ''

        if image is not None:
            note2 = '[INFO] Suspect image attached.'.upper()

            attachment = open((image), "rb")
            part = MIMEBase("application", "octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            filename = os.path.split(image)[-1]
            part.add_header("Content-Disposition", "attachement; filename= %s" % filename)
            msg.add_alternative(part)
            attachment.close()
        HTML_MESSAGE = """\
                            <html>
                            <head></head>
                            <body>
                                <h1 style="text-align: center;">&nbsp; &nbsp; <font size="10">SECURITY ALERT</font></h1>
                                <h1 style="text-align: center;"><strong><img src="https://upload.wikimedia.org/wikipedia/sl/thumb/1/1c/Polje_pomembno.svg/400px-Polje_pomembno.svg.png" alt="" width="242" height="242" align="middle" /></strong></h1>
                                <h1 style="text-align: center;">&nbsp; &nbsp;[AN UNKNOWN PERSON HAS BEEN DETECTED IN YOUR PREMISES]</h1>
                                <h1 style="text-align: center;"><font size="4">[ LOCATION ]: <mark>place</mark></font>&nbsp;&nbsp;<font size="4">[ TIME ]: <mark>when</mark></font></h1>
                                <h1 style="text-align: center;"><font size="3">{}</font></h1>
                                <h1 style="text-align: center;"><font size="3">{}</font></h1>
                                <h1 style="text-align: center;"><font size="3">{}</font></h1>
                            </body>
                            </html>
                                   """.format(config.camip,note2, note1)
        HTML_MESSAGE = HTML_MESSAGE.replace('when', timestamp)
        HTML_MESSAGE = HTML_MESSAGE.replace('place', location)
        msg.add_alternative(HTML_MESSAGE, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.login(username, password)
            smtp_server.send_message(msg)
            if image is not None:
                print('[INFO] Image of suspect is attached.'.upper())

            print('[INFO] Email sent successfully.'.upper())
