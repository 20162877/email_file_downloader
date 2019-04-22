#Hi I am Zaid Ahmad pursuing MCA from JAMIA MILLIA ISLAMIA
#THIS CODE IS WRITTEN TO DOWNLOAD ALL ATTACHMENTS AND PLAIN TEXT(BODY) FROM GMAIL OR OTHER EMAIL CLIENTS AND
#SAVE THEM INTO THEIR CORRESPONDING LOCAL FOLDERS(THE FOLDER NAME IS SET TO SENDER'S EMAIL ADDRESS)
#ANYONE CAN DOWNLOAD IT,MODYFY IT BASED ON THEIR REQUIREMENTS
#THE FOLLOWING CODE IS FREE TO DOWNLOAD AND USE FOR COMMERCIAL AND NON COMMERCIAL PURPOSE 
#IN CASE OF ANY QUERY FEEL FREE TO ASK.
#CONTACT NUMBER: +91 8585971473(WHATS APP), +91 7570929942
# EMAL: syedzaidahmad99@gmail.com
import email
import getpass, imaplib
import os

detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

#Change directory into attachments
os.chdir('attachments')

uName = input('Enter your GMail username:')
pwd = getpass.getpass('Enter your password: ')


imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login(uName,pwd)
print("Login Successfull")

if typ != 'OK':
    print('Not able to sign in!')
    raise
print("Labels in {}:".format(uName))

LabelList = list(enumerate(imapSession.list()[1]))

#To List number of Labels 
for label in LabelList: 
	print(label)

#Type label
lbl = input("Type Label to select: ")

# To Select specific label
data = imapSession.select(lbl)[1]

print(lbl+" selected")
print("{} Emails are in {}".format(str(data[0])[2:-1],lbl))

#Search all email in specific label
typ,data = imapSession.search(None, 'ALL')

email_item_list=data[0].split()
print(email_item_list)
for id in email_item_list:
	typ, msg = imapSession.fetch(id,'(RFC822)')
	msgBody = msg[0][1].decode('utf-8')
	email_msg = email.message_from_string(msgBody)
	#print(dir(email_msg))

	print("Subject: ",email_msg['Subject'])
	print("From: ",email_msg['From'])
	print("To: ",email_msg['To'])
	print("Date: ",email_msg['Date'])
#	print(dir(email_msg))
	if email_msg['From'] not in os.listdir():#If senders name directory present
	   os.mkdir(email_msg['From']) #Creating directory of senders name
	
	for part in email_msg.walk():
		 print("Content Type: ",part.get_content_type())
	#	 print("Content Values: ",part.values())
		 print("Content items: ",part.items()) 
		 filename = part.get_filename()
		 print(filename)
	#	 print("Pay Load: ",part.get_payload(decode=True))
		 if part.get_content_type().split('/')[0] in ['text','application']:# Check All Text masseges and files

		   if part.get_content_type().split('/')[1] in ['plain']  and not (filename=='None'):# Check only plain Text (writtten below subject)

		    open(email_msg['From']+'/'+email_msg['Subject'].replace('/','_'),'wb').write(part.get_payload(decode=True)) 

		   elif part.get_content_type().split('/')[1] not in ['html']:# Check Attachments that are in text form. like .txt etc

		    open(email_msg['From']+'/'+filename.replace('/','_'),'wb').write(part.get_payload(decode=True)) 

		    print("Contents has been witten in {}".format(email_msg['From']))
		 if part.get_content_type().split('/')[0] in ['image']:# Check attachments that are in image form

		  open(email_msg['From']+'/'+filename.replace('/','_'),'wb').write(part.get_payload(decode=True))
imapSession.close()
imapSession.logout()
