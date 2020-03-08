"""
*** Duc Dao ***
About This Script:
app send mail - connect to gmail and send mail
"""

import smtplib, ssl, socket

def email_send(url_L, recipients_L):  # need to print out msg dialog in GUI
	try:
		# connect to Gmail (cre[line 7~10]: realpython.com )
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo_or_helo_if_needed()  # Identify yourself to an ESMTP server using ehlo or helo
		server.starttls(context=ssl.create_default_context())  # Create a secure SSL context connection
		server.ehlo_or_helo_if_needed()

		# try to login
		server.login("server.testing.0807@gmail.com", "sxnjrssijparndpn")

	except socket.gaierror:  # no server connection / wrong host name
		print("Please Check Your Internet Connection")

	except smtplib.SMTPAuthenticationError:  # wrong login info
		print("Gmail Address or Password is Incorrect")

	except smtplib.SMTPSenderRefused:
		print("Their Are Something Wrong With The Server, Try Later")

	except smtplib.SMTPRecipientsRefused:
		print("Recipient Email Address Not Correct")

	except:
		print("Something Went Wrong:")

	else:  # sending message
		subject = "Item Price Fell Down"
		body = f"""The item price has fallen under your desired price
		\nYou can buy the product using this link: {url_L}"""

		msg = f"Subject:{subject}\n\n{body}"
		server.sendmail("server.testing.0807@gmail.com", recipients_L, msg)
		print("\nEmail Send Success")

	finally:
		server.quit()
