"""

** coded by shibinmak on 1/10/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import cv2
import os
import imutils
import json
import config
from Alerts.Email import EmailAlert
from Alerts.SMSAlert import SMSAlert
from Alerts.whatsapp import WhatsApp
import numpy as np
from collections import deque, OrderedDict
import datetime


model = config.model
protoxt = config.prototxt
minc = 0.3
sms = SMSAlert()
email = EmailAlert()
whatsapp = WhatsApp()

CLASSES = json.loads(open(config.classes).read())

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe(protoxt, model)
counter = 0

cap = cv2.VideoCapture(config.video)
iobjects = ["person", "motorbike", "car", "dog", "bicycle"]
framedeque = deque(maxlen=2)
personlog = OrderedDict()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    copy = frame
    frame = imutils.resize(frame, width=600)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()
    if counter > 0:
        timeout = personlog[counter] + datetime.timedelta(seconds=60)
        if datetime.datetime.now() > timeout:
            print("[INFO] RESETTING COUNTER & CLEARING RESOURCES..")
            counter = 0
            personlog.clear()
            framedeque.clear()

    for i in range(0, detections.shape[2]):
        print("[INFO] COUNTER= {}".format(counter))

        confidence = detections[0, 0, i, 2]

        if confidence > minc:

            idx = int(detections[0, 0, i, 1])

            if CLASSES[idx] in iobjects:

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                object = CLASSES[idx]

                label = "{}:{:.2f}%".format(object, confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                labelsize = cv2.getTextSize(label, font, 0.75, 2)[0]
                Y = startY - labelsize[1] if startY - labelsize[1] > 10 else startY
                X = int(startX + (endX - startX) / 2)
                cv2.putText(frame, label, (X, Y), font, 0.50, (0, 0, 255), 2)
                if counter == 0 and object == 'person':
                    counter += 1
                    personlog[counter] = datetime.datetime.now()
                    framedeque.append(frame)
                    timestamp = str(datetime.datetime.now().strftime("%d-%b-%Y|%H:%M:%S").upper())
                    fname = os.path.join(config.datafolder, timestamp + '.jpg')
                    print('\n[INFO] SECURITY ALERT.')
                    print('[INFO] {}'.format(fname))
                    cv2.imwrite(fname, frame)
                    whatsapp.sendWhatsApp()
                    sms.SendSMS()
                    email.SendEmail(image=fname)
                    # warningsize = cv2.getTextSize("EMERGENCY ALERT SEND", font, 2, 2)[0]
                    # Y = warningsize[1]
                    # X = int(w/2)
                    # cv2.putText(frame, "EMERGENCY ALERT SEND", (X, Y), font, 2, COLORS[idx], 2)
                    os.remove(fname)

                elif counter > 0 and object == 'person':
                    # previousframetime
                    delay = personlog[counter] + datetime.timedelta(seconds=30)
                    ic = np.array_equal(framedeque[-1],
                                        frame)  # identity check between current frame and previous frame

                    if not ic and object == 'person' and datetime.datetime.now() > delay:
                        print('\n[INFO] SECURITY ALERT.')
                        counter += 1
                        framedeque.append(frame)
                        personlog[counter] = datetime.datetime.now()
                        timestamp = str(datetime.datetime.now().strftime("%d-%b-%Y|%H:%M:%S").upper())
                        fname = os.path.join(config.datafolder, timestamp + '.jpg')
                        print('[INFO] {}'.format(fname))
                        cv2.imwrite(fname, frame)
                        whatsapp.sendWhatsApp()
                        email.SendEmail(image=fname)
                        os.remove(fname)
                        '''framedeque.append(frame)
                        if counter >3:
                            for i,img in enumerate(framedeque):
                                timestamp = str(datetime.now().strftime("%d-%b-%Y|%H:%M:%S").upper())
                                fname=os.path.join(config.datafolder,timestamp+i+'.jpg')
                                cv2.imwrite(fname,img)
                                email.SendEmail(image=fname)'''

    cv2.imshow("SECURITY SYSTEM", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
