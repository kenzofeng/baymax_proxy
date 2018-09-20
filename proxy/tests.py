import smtplib
import env
from email.mime.text import MIMEText

sender = env.SENDER
subject = '1_Regression_Test_1'
smtpserver = env.SMPT
username = env.USERNAME
password = env.PWD
msg = MIMEText("aaaaaa")
msg['Subject'] = subject
smtp = smtplib.SMTP_SSL(smtpserver,env.email_port)
smtp.login(username, password)
smtp.sendmail(sender, 'daniel.liu@derbysoft.com', msg.as_string())
smtp.quit()