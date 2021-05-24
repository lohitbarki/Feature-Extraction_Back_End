import feedparser
import string
from csv import writer
from csv import reader
import pandas as pd
import socket
import io
import pickle

INPUT_DIR = "C:/wamp64/www/ApplyRules/Input"
OUTPUT_DIR = "C:/wamp64/www/ApplyRules/Output"

SUBSCRIBER_LIST = INPUT_DIR + '/subscriberList.txt'
TRAINING_DATASET = INPUT_DIR + '/RSSDataset.csv'
TESTING_DATASET = INPUT_DIR + '/feedsRead.csv'
TESTING_DATASET_WITH_INFO = INPUT_DIR + '/feedsWithInfo.csv'
PREDICATED_DATASET = OUTPUT_DIR + '/PredictedResults.csv'

HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
PORT = "8090"
LOCALHOST = "http://" + IPADDRESS + ":" + PORT + "/ApplyRules"
SERVER_INPUT = LOCALHOST + '/Input/RSSDataset.csv'
SERVER_OUTPUT = LOCALHOST + '/Output/PredictedResults.csv'

def getSubscriberList():
    return SUBSCRIBER_LIST


def getTrainingDataSet():
    return TRAINING_DATASET


def getTestingDataSet():
    return TESTING_DATASET


# Returns training data
def getTrainingData():
    TRAINING_DATA = pd.read_csv(getTrainingDataSet(), encoding='unicode_escape', sep=',', names=["Feature", "Label"])
    return TRAINING_DATA


# Returns testing data
def getTestingData():
    TESTING_DATA = pd.read_csv(getTestingDataSet(), encoding='unicode_escape', sep=',', names=["Feature"])
    return TESTING_DATA


# Process text from file
def text_process(mess):
    token = [char for char in mess if char not in string.punctuation]
    token = ''.join(token)
    with open(INPUT_DIR + '/english_words.pickle', 'rb') as fobj:
        english_stop_words = pickle.load(fobj)

    # return [word for word in token.split() if word.lower() not in stopwords.words('english')]

    return [word for word in token.split() if word.lower() not in english_stop_words]


# Create file with predicted values
def generatePredictFile(all_predictions):
    i = 0
    with io.open(TESTING_DATASET_WITH_INFO, 'r',encoding="utf-8") as read_obj, \
            io.open(PREDICATED_DATASET, 'w', newline='',encoding="utf-8") as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        for row in csv_reader:
            if i == 0:
                row.append('Label')
            else:
                row.append(all_predictions[i])
            i = i + 1
            csv_writer.writerow(row)
    return i


def post_is_in_db(title):
    with io.open(TESTING_DATASET, 'r',encoding="utf-8") as database:
        for line in database:
            if title in line:
                return True
    return False


def dumpDataFromRSSFeed(url):
    feed = feedparser.parse(url)
    f_test = io.open(TESTING_DATASET, 'w', encoding="utf-8")
    f_test_info = io.open(TESTING_DATASET_WITH_INFO, 'w', encoding="utf-8")

    f_test_info.write('Feature' + ',' + 'Published' + ',' + 'Link' + '\n')
    f_test.write('Feature' + '\n')
    for post in feed.entries:
        # if post is already in the database, skip it
        # TODO check the time
        feedTitle = post.title
        feedLink = post.link
        feedTime = post.published

        if not feedTitle.startswith("FIX"):
            feedTitle = feedTitle.replace(',', '')
            feedTitle = feedTitle.replace('\n', ' ')
            feedTime = feedTime.replace(',', '')
            if not post_is_in_db(feedTitle):
                f_test.write(feedTitle + '\n')
                f_test_info.write(feedTitle + ',')
                f_test_info.write(feedTime + ',')
                f_test_info.write(feedLink + "\n")
    f_test.close()
    f_test_info.close()

def getHTMLPage(i):

    message = "<html><h2>List of Features</h2>"

    message = message + '<p>RSS Feed list : <a href=' + SERVER_OUTPUT + '>' + ' Download</a></p>'
    message = message + '<p>Training Dataset : <a href=' + SERVER_INPUT + '>' + ' Download</a></p>'
    message = message + '<body><br>'

    j = 0
    OUTPUT_DATA = pd.read_csv(PREDICATED_DATASET, encoding='unicode_escape', sep=',',
                              names=["Feature", "Published", "Link", "Label"])

    # Check for the feature list
    while j < i:
        if OUTPUT_DATA['Label'][j] == "feature":
            message = message + '<hr>' + OUTPUT_DATA['Published'][
                j] + '&nbsp&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp' + '<a href= ' \
                      + OUTPUT_DATA['Link'][j] + '>' + OUTPUT_DATA['Feature'][j].strip() + "</a></hr>"
        j = j + 1

    message = message + "</body></html>"
    return message

def openTab(message):
    import webbrowser
    f = io.open(OUTPUT_DIR + '/Features.html', 'wb')

    f.write(message.encode())
    f.close()
    webbrowser.open_new_tab(OUTPUT_DIR + '/Features.html')
