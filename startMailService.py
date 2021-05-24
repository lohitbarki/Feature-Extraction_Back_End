from Mail.sendMail import send_email
from General.Connection import emailList
from General.Connection import userSubscribedFeed
from General.Connection import getPredictedFeedOutput

subscriberList = emailList()


for subscriber in subscriberList:
    subscriber = ''.join(subscriber)
    suscribedFeedList = userSubscribedFeed(subscriber)

    for feed in suscribedFeedList:
        feed = ''.join(feed)
        feedOutput = getPredictedFeedOutput(feed)
        #print(subscriber)
        #print(feedOutput)
        send_email(subscriber, feedOutput)