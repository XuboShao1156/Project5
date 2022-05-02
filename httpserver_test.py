import csv
import random

import requests

# replica = 'p5-http-a.5700.network'
replica = 'localhost'

pageviews = []
with open('pageviews.csv') as f:
    for row in csv.reader(f):
        pageviews.append((row[0], int(row[1])))

def test(server, session, page):
    resp = session.get('http://{}:40007/{}'.format(server, page[0]))
    if resp.status_code != 200:
        print('\tERROR for {}!'.format(page))
    print('\t{} for {}.'.format(resp.status_code, page))


def serial_test(server, freq, min_freq=0):
    session = requests.session()
    for idx, page in enumerate(freq):
        print('{}.testing {}...'.format(idx, page))
        test(server, session, page)


def random_test(server, freq, size=5000):
    session = requests.session()
    for idx in range(1, size + 1):
        page = freq[random.randint(0, len(freq)-1)]
        print('{}.testing {}...'.format(idx, page))
        test(server, session, page)


if __name__ == '__main__':
    serial_test(replica, pageviews)
    # random_test(replica, pageviews, size=100)