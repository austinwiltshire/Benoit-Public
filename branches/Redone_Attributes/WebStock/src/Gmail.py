from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

def sendMail(body, subject=None, _from=None, to="john.a.graham@gmail.com", userName="work.jgraham@gmail.com", userPassword="ram777"):
	
	if not _from:
		_from = userName

	msg = MIMEMultipart()
	msg['From'] = userName
	msg['To'] = to
	msg['Subject'] = subject
	msg.attach(MIMEText(body))
	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(userName, userPassword)
	mailServer.sendmail(userName, to, msg.as_string())
	mailServer.close()
	