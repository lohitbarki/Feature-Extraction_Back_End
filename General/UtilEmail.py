import smtplib, ssl

port = 25  # For SSL
smtp_server = "mail.informatica.com"
sender_email = "lbarki@informatica.com"  # Enter your address


# Send mail to the subscribers
def sendMail(receiver_email, message):
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.sendmail(sender_email, receiver_email, message.as_string())

    except AssertionError as error:
        print(error)
        print("Something went wrong...")