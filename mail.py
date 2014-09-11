# automated email with file attachment module 
# Author:Colin 
# reference: http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python
# Date: Nov 18 2013



import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(sentfrom,to,subject,text,files=[],server='smtp.gmail.com:587',
	user = 'colin.brat@gmail.com',password='colin89757'):
	"generate automated email to a client using Gmail, by default colin's Gmail. "
	assert type(to) == list
	assert type(files) == list 
	
	msg = MIMEMultipart() 
	msg['From'] = sentfrom 
	msg['To'] = COMMASPACE.join(to) 
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject 

	msg.attach(MIMEText(text))

	for f in files:
		part  = MIMEBase('application', "octet-stream")
		part.set_payload(open(f,'rb').read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)
	try:
		smtp_s = smtplib.SMTP(server)
		smtp_s.ehlo()  
		smtp_s.starttls()
		smtp_s.login(user, password)
		smtp_s.sendmail(sentfrom, to, msg.as_string() )
		smtp_s.close()
		print "successfully sent the mail !"
	except:
		print 'failed to send a mail ' 
			
	


if __name__ == '__main__':
	# files = ['E:\\Archive\\Career and Profession\\Job Seeker Kit\\resumes\\Final Sample\\arm_hlin.docx']
	sentfrom=raw_input("sent as(sender display name): \n")

	subject = raw_input('subject : \n')
	text = 'hello this is a automated python mail '
	files = []
	to=raw_input('recipient email address: \n')
	to = [to]

	print 'ready to send the mail !'
	send_mail(sentfrom,to,subject,text,files) 
	print 'email sent!'


