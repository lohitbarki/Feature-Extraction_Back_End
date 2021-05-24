from General.Connection import insertEmail
from Mail.sendMail import subscription_email
import sys

emailID = sys.argv[1];

if(insertEmail(emailID)):
    subscription_email(emailID)