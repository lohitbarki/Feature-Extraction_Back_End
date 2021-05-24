from General.Connection import getSubscriptionList
import sys

emailID = sys.argv[1];

feedList = getSubscriptionList(emailID)

final_result = [list(i) for i in feedList]

if len(final_result) == 0:
    print('Empty!!')
else:
    list = "<ul>"
    for i in final_result:
        val = ''
        list = list + "<li >" + val.join(i) + "</li>"

    list = list + '</ul>'

    print(list)

