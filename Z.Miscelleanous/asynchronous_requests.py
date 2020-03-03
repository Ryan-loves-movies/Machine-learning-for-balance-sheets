# One of the codes I found online but which I did not find useful as it uses http connection which I'm
# of whether I'm using or not??

from urllib import parse
from threading import Thread
import http, sys
from queue import Queue
from all_stock_symb import tasks
from convert_finance_num import convert_num
from urllib.request import urlopen
import json

debt_free_companies = []
concurrent = 200
q = Queue(concurrent * 2)

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """

    response = urlopen(url)
    data = response.read().decode("utf-8")
    symbol = url[76:len(url)]
    return json.loads(data), symbol

def doSomethingWithResult(data, url):
    if data != {}:
        debt = convert_num(data['financials'][0]['Total debt'])
        if debt == 0:
            debt_free_companies.append(url)

def doWork():
    while True:
        url = q.get()
        status, url = get_jsonparsed_data(url)
        doSomethingWithResult(status, url)
        q.task_done()


for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

try:
    for url in tasks:
        q.put(url)
    q.join()
print(q)

except KeyboardInterrupt:
    sys.exit(1)

print(debt_free_companies)