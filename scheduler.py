#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from random import randint
import csv
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib, ssl
import schedule
import random
import time

from script import content1, content2, title1, title2

client = MongoClient(port=27017)
db = client.business


def getMails():
    with open("/home/alex/Connections.csv", 'rt',encoding="utf-8") as csvfile:
        connectlist = []
        reader = csv.DictReader(csvfile)
        for row in reader:

            email = row['Email Address'].strip()
            firstName = row['First Name']
            lastName = row['Last Name']
            company = row['Company']
            positon = row['Position']

            context = """Hi,""" + firstName + content2
           
            context = context.strip()
            business = {
                'title': title2,
                'firstName': firstName,
                'lastName': lastName,
                'position': positon,
                'email': email,
                'context': context
            }
            connectlist.append(business)
            
            if email:
                conn = db.ads.find({"email": email}).count()
                print(conn)
                if conn == 0:
                   result = db.ads.insert_one(business)
           


def sendMails():

        # result = db.reviews.find({"position":{"$in":['Co-Founder','Developer']}})
        result = db.ads.find({"flag": {"$ne": "true"}}).limit(1);
        # result = db.ads.find({"position": {"$in": ['Co-Founder','CEO', 'Manager', 'VP', 'chairman', 'Founder', 'COO', 'Sales Director', 'Sale', 'President', 'real Estate', 'Estate', 'self-employed']}})
        # print(result)

        try:
            mail_host = "smtp.gmail.com"
           
            mail_user = "#youruser"
            mail_pass = "#yourpassword"
            mail_postfix = "gmail.com"

           

            s = smtplib.SMTP_SSL(mail_host, 465)
           
            s.ehlo()
            print("begin---connecting")
           
            print("connecting")
            s.login(mail_user, mail_pass)
            print("connected")

            for item in result:
                tic = time.time()

                me = "Alex Wang<swoecwang10@gmail.com>"  # +self.mail_user #+"<"+ self.mail_user + "@"+self.mail_postfix
               
                msg = MIMEMultipart()
                msg['Form'] = me
                msg['To'] = item['email']
               
                msg['Subject'] = item['title']
                context = item['context']
                for x in context:
                    
                    puretext = MIMEText(x)

                puretext = MIMEText(str(context))
               
                msg.attach(puretext)

                # jpg attached
                # jpgpart = MIMEApplication(open('/home/alex/3962.jpg', 'rb').read())
                # jpgpart.add_header('Content-Disposition', 'attachment', filename='3962.jpg')
                # msg.attach(jpgpart)
                # part = MIMEApplication(open('/home/alex/cv/Alex Wang-A-Full stack.pdf', 'rb').read())
                # part.add_header('Content-Disposition', 'attachment', filename="Alex Wang-A-Full stack.pdf")
                # msg.attach(part)
                receiver = item['email']
               
                

                time.sleep(13*random.random())
                s.sendmail(me, receiver, msg.as_string())
                # toc = time.time()
                # print("send mail in"+ {toc - tic}+" seconds")
                newvalues = {"$set": {"flag": "true"}}
                db.ads.update_one(item, newvalues)
            print("---send---")
            s.close()

        except Exception as e:
            print(str(e))

schedule.every(1).minutes.do(getMails)
schedule.every(1).minutes.do(sendMails)

# schedule.every().day.at("12:00").do(sendMails)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
