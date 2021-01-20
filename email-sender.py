#cz1529
from socket import *
import ssl
import base64
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def main():
	#get socket server/port
	mail_server=input('Enter a mail server (otherwise default will be gmail):')
	if(mail_server==''):
		mail_server = 'smtp.gmail.com'

	port=input('Enter socket port (otherwise default will be 465):')
	if(port==''):
		port = 465

	clientSocket = socket(AF_INET, SOCK_STREAM)

	# connect to mail server
	clientSocket = ssl.wrap_socket(clientSocket)
	clientSocket.connect((mail_server, port))
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '220':
		print('220 reply not received from server.')

	# Send EHLO
	clientSocket.send('EHLO localhost\r\n'.encode())
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '250':
		print('250 reply not received from server.')

	# authentication
	username = input("Enter your email: ")
	password = input("Enter your password: ")
	base64_str = ('\x00'+username+'\x00'+password).encode()
	base64_str = base64.b64encode(base64_str)
	authMsg = 'AUTH PLAIN '.encode()+base64_str+'\r\n'.encode()
	clientSocket.send(authMsg)
	recv = clientSocket.recv(1024).decode()
	print(recv)

	# MAIL FROM command
	mailFrom='MAIL FROM: <'+username+'>\r\n'
	clientSocket.send(mailFrom.encode())
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '250': #if the data is not received
		print('250 reply not received from server.')

	# RCPT TO command
	sendToUser=input("Enter the email you want to send a message to: ")
	mailTo='RCPT TO: <'+sendToUser+'>\r\n'
	clientSocket.send(mailTo.encode())
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '250':
		print('250 reply not received from server.')

	# DATA command
	clientSocket.send('DATA\r\n'.encode())
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '354':
		print('250 reply not received from server.')



	# message to send
	imgData = open('./cat.png', 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = 'CS4793'
	msg['From'] = username
	msg['To'] = sendToUser

	text = MIMEText("Connies Extra Credit Assignment")
	msg.attach(text)
	image = MIMEImage(imgData, name=os.path.basename('./cat.png'))
	msg.attach(image)

	endmsg = '\r\n.\r\n'


	# Send message data.
	clientSocket.send(msg.as_string().encode())

	# Message ends
	clientSocket.send(endmsg.encode())
	recv = clientSocket.recv(1024).decode()
	print(recv)
	if recv[:3] != '250':
		print('250 reply not received from server.')

	# QUIT connection
	clientSocket.send('QUIT\r\n'.encode())
	clientSocket.close()

main()
