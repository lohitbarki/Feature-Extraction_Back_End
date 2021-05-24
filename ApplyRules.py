from sklearn.feature_extraction.text import CountVectorizer
from General.Utils import dumpDataFromRSSFeed
from General.Utils import getTrainingData, getTestingData
from General.Utils import text_process
from General.Utils import generatePredictFile
from General.Utils import openTab
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from General.Utils import getHTMLPage
from General.Connection import updateOutput
from General.Connection import addUserFeed
from Mail.sendMail import send_instant_email
from General.Connection import getFeedNamFromURL

import sys

# Getting all info from RSS feed

#feed_name = 'SQL Server 2016'
#url = 'https://support.microsoft.com/app/content/api/content/feeds/sap/en-in/d201c5bd-9aab-36d1-0e57-5dadf52a6dad/rss';

url = sys.argv[1]
print('Getting info from : ' + url)
print(getFeedNamFromURL(url))

url = sys.argv[1];
emailID = sys.argv[3];

flag = 0;
#flag = sys.argv[1];

dumpDataFromRSSFeed(url)

# Read training and testing data

TRAINING_DATA = getTrainingData()
TESTING_DATA = getTestingData()

# Training model

training_bow_transformer = CountVectorizer(analyzer=text_process).fit(TRAINING_DATA['Feature'].values.astype('U'))

messages_bow = training_bow_transformer.transform(TRAINING_DATA['Feature'].values.astype('U'))

tfidf_transformer = TfidfTransformer().fit(messages_bow)

messages_tfidf = tfidf_transformer.transform(messages_bow)

spam_detect_model = MultinomialNB().fit(messages_tfidf, TRAINING_DATA['Label'])

# Predicting values

#testing_bow_transformer = CountVectorizer(analyzer=text_process).fit(TESTING_DATA['Feature'].values.astype('U'))

predict_bow = training_bow_transformer.transform(TESTING_DATA['Feature'].values.astype('U'))

predict_transformer = TfidfTransformer().fit(predict_bow)

predict_tfidf = predict_transformer.transform(predict_bow)

all_predictions = spam_detect_model.predict(predict_tfidf)

i = generatePredictFile(all_predictions)

message = getHTMLPage(i)

openTab(message)

print(message)

updateOutput(url, message)

addUserFeed(emailID, url);

send_instant_email(emailID, message)

# yet to implement

#verfifyResults()

#appendResultToTrainingDataset()