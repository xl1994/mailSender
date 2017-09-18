#!/usr/bin/python
# -*- Coding: UTF-8 -*-

'''
Before using this demo, you should apply for an client authentication in netease mail service
and use the authentication code to login rather than your password of the account
'''

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

def sender_init():
    # auth code ******
    mail_host = 'smtp.163.com'
    user = '18613029274@163.com'
    pwd = '******'
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(user,pwd)
    except smtplib.SMTPException as e:
        print("Error: Initiation Failed\n", str(e))
    return smtpObj

def message_init(subject, receviers):
    user = '18613029274@163.com'
    message = MIMEMultipart()
    message['From'] = "{}".format(user)
    message['To'] = ",".join(receviers)
    message['Subject'] = subject
    return message

def message_add_text(message, text):
    message.attach(MIMEText(text,'plain','utf-8'))
    return message

def message_add_html(message, html):
    message.attach(MIMEText(html,'html','utf-8'))
    return message

def message_add_image(message, image):
    with open(image, 'rb') as f:
        mime = MIMEBase('image', 'png', filename=image)
        mime.add_header('Content-Disposition', 'attachment', filename=image)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        message.attach(mime)
    return message


def sender_send(smtpObj, message, receviers):
    user = '18613029274@163.com'
    flag = True
    try:
        smtpObj.sendmail(user, receviers, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('Error: Send Failed\n', str(e))
        flag = False
    return flag

if '__main__' == __name__:
    snder = sender_init()
    subject = 'Python SMTP 邮件测试'
    receviers = ['champion556@163.com']
    msg = message_init(subject, receviers)
    text = 'Python 邮件发送测试...'
    msg = message_add_text(msg, text)
    sender_send(snder, msg, receviers)
    print("邮件发送成功")


