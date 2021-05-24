import mysql.connector as mdb
from mysql.connector import Error

DBNAME = "feature"
DBHOST = "localhost"
DBPWD = ""
DBUser = "root"

def connect():
        connection = mdb.connect(host=DBHOST,
                                 database=DBNAME,
                                 user=DBUser,
                                 password=DBPWD)

        mySql_Create_Table_Query = "insert into email_list(email) values('wxyz@com')"
        return connection

def getVendorAllList ():
    try:
        connection = connect()
        selectQuery = "select name from vendor;"
        #print(selectQuery)
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        return result

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def inserVendor(vendor):
    try:
        connection = connect()
        insertQuery = "insert into vendor(name) values('" +  vendor + "');"
        #print(insertQuery)
        cursor = connection.cursor()
        result = cursor.execute(insertQuery)
        connection.commit();
        print("Added vendor successfully!!")
        return cursor.lastrowid;
    except mdb.Error as error:
        #print("Failed to select data in MySQL: {}".format(error))
        print("Already vendor added!!")
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def inserVersion(version, url, vendor_id):
    try:
        connection = connect()
        insertQuery = "insert into feed(feed_name, url, vendor_id) values('" +  version + "','" + url  + "','" + vendor_id + "');"
        #print(insertQuery)
        cursor = connection.cursor()
        result = cursor.execute(insertQuery)
        connection.commit();
        print("Added version successfully!!")
        return 1;
    except mdb.Error as error:
        #print("Failed to select data in MySQL: {}".format(error))
        print("Already version added!!")
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertEmail(emailID):
    try:
        connection = connect()
        insertQuery = "insert into email_list(email) values('" +  emailID + "');"
        #print(insertQuery)
        cursor = connection.cursor()
        result = cursor.execute(insertQuery)
        connection.commit();
        print("Subscribed successfully!!")
        return 1;
    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        print("Already subscribed!!")
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def removeEmail(emailID):
    try:
        connection = connect()
        deleteQuery = "delete from email_list where email = '" + emailID + "';"
        #print(deleteQuery)
        cursor = connection.cursor()
        result = cursor.execute(deleteQuery)
        connection.commit();
        print("Unsubscribed successfully!!")
        return 1;
    except mdb.Error as error:
        print("Subscription not found!!")
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateOutput(url, output):
    try:
        connection = connect()
        updateQuery = "UPDATE feed SET predictedList='" + output + " ' WHERE url='" + url + "';"
        cursor = connection.cursor()
        result = cursor.execute(updateQuery)
        connection.commit();
        #print("Updated successfully!!")
        return 1;
    except mdb.Error as error:
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def emailList ():
    try:
        connection = connect()
        selectQuery = "select email from email_list;"
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        finalList = [list(i) for i in result]
        #print("Select successfull !!")
        return finalList

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()




def getSubscriptionList (email):
    try:
        connection = connect()
        selectQuery = "select feed_name from feed where url in (select feedURL from email_feed where emailID = '" + email + "');"
        #print(selectQuery)
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        return result

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def addUserFeed(emailID, url):
    try:
        connection = connect()
        insertQuery = "insert into email_feed values('" +  emailID + "','"+ url + "');"
        #print(insertQuery)
        cursor = connection.cursor()
        result = cursor.execute(insertQuery)
        connection.commit();
        #print("Inserted successfully!!")
        return 1;
    except mdb.Error as error:
        #print("Failed to select data in MySQL: {}".format(error))
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



def userSubscribedFeed (email):
    try:
        connection = connect()
        selectQuery = "select feedURL from email_feed where emailID  = '" + email + "';"
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        return result

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



def getPredictedFeedOutput (feedURL):
    try:
        connection = connect()
        selectQuery = "select predictedList from feed where url  = '" + feedURL + "';"
        #print(selectQuery)
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        return result[0][0]

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



def getFeedNamFromURL (feeURL):
    try:
        connection = connect()
        selectQuery = "select feed_name from feed where url = '" + feeURL + "';"
        #print(selectQuery)
        cursor = connection.cursor()
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        return result

    except mdb.Error as error:
        print("Failed to select data in MySQL: {}".format(error))
        return 0;

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()