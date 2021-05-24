from General.UtilEmail import sendMail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "FeatureList@informatica.com"  # Enter receiver address
dev_email = "lbarki@informatica.com"

message = MIMEMultipart("alternative")
message["Subject"] = "New features list"
message["From"] = sender_email

text = """\
List of features:"""

def send_email(receiver_email, msg):

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(msg, "html")

    message.attach(part1)
    message.attach(part2)

    print(receiver_email)
    print(message)
    sendMail(receiver_email, message)


def send_instant_email(recieverMail, msg):
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(msg, "html")

    message.attach(part1)
    message.attach(part2)

    sendMail(recieverMail, message)


def subscription_email(mail):
    sub_message = MIMEMultipart("alternative")
    sub_message["Subject"] = "Subscription to features list"
    sub_message["From"] = sender_email

    sub_text = """\
    Suscribed sucessfully : """ + mail

    part1 = MIMEText(sub_text, "plain")

    sub_message.attach(part1)

    sendMail(mail, sub_message)
    sendMail(dev_email, sub_message)



def unsubscription_email(mail):
    sub_message = MIMEMultipart("alternative")
    sub_message["Subject"] = "Unubscription to features list"
    sub_message["From"] = sender_email

    sub_text = """\
    Unsuscribed sucessfully : """ + mail

    part1 = MIMEText(sub_text, "plain")

    sub_message.attach(part1)

    sendMail(mail, sub_message)
    sendMail(dev_email, sub_message)
