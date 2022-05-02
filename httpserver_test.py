import csv
import requests

replica = 'p5-http-a.5700.network',

session = requests.session()
with open('pageviews.csv') as f:
    for row in csv.reader(f):
        if int(row[1]) > 0:
            resp = session.get('http://{}:40007/{}'.format(replica, row[0]))
            print("{} for {}".format(resp.status_code, row[0]))
