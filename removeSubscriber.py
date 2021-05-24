from General.Connection import removeEmail
from Mail.sendMail import unsubscription_email

import sys

emailID = sys.argv[1];

if(removeEmail(emailID)):
    unsubscription_email(emailID)