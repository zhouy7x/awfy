import smtplib
import sys
import email.mime.text

recipients = [
    "li1.chen@intel.com",
]

sender = "awfy-user"


def sendHtmlMail(header, content):
    mail_username = 'APKAutoBuildNotification@intel.com'
    mail_password = 'whatever'

    HOST = 'smtp.intel.com'
    PORT = 25

    # Create SMTP Object
    smtp = smtplib.SMTP()
    print 'connecting ...'

    # show the debug log
    smtp.set_debuglevel(1)

    # connet
    try:
        print smtp.connect(HOST, PORT)
    except:
        print 'CONNECT ERROR ****'

    # login with username & password
    try:
        print 'loginning ...'
        smtp.login(mail_username, mail_password)
    except:
        print 'LOGIN ERROR ****'
    # fill content with MIMEText's object   
    mailMessage = '''<html>
    <head> <title>Awfy Notification</title></head>
    <body>
    <h1>Awfy Notification</h1>
    <h2>%s</h2>
    <p>%s</p>
    </body>
    </html>''' % (header, content)

    msg = email.mime.text.MIMEText(mailMessage, 'html')
    msg['From'] = sender
    msg['To'] = recipients[0]
    msg['Subject'] = 'Awfy Notification.'

    smtp.sendmail(mail_username, recipients, msg.as_string())
    smtp.quit()


sendHtmlMail('kk', 'aaa')
