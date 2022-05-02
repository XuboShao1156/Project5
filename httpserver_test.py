import concurrent.futures
import csv
import random
import time
import requests

replicas = [
    # 'p5-http-a.5700.network',
    # 'p5-http-b.5700.network',
    # 'p5-http-c.5700.network',
    # 'p5-http-d.5700.network',
    # 'p5-http-e.5700.network',
    # 'p5-http-f.5700.network',
    # 'p5-http-g.5700.network',
    'localhost'
]

pageviews = []
with open('pageviews.csv') as f:
    for row in csv.reader(f):
        pageviews.append((row[0], int(row[1])))

def test(server, session, idx, page):
    resp = session.get('http://{}:40007/{}'.format(server, page[0]))
    if resp.status_code != 200:
        print('ERROR for {} on {}!'.format(page, server))
    print('{}. code {} for {} on {}.'.format(idx, resp.status_code, page, server))


def serial_test(server, freq, min_freq=0):
    start = time.time()
    session = requests.session()
    for idx, page in enumerate(freq):
        if page[1] < min_freq:
            break
        test(server, session, idx + 1, page)
    print('finished serial test on replica {} in {}'.format(server, time.time() - start))


def random_test(server, freq, size=5000):
    session = requests.session()
    for idx in range(1, size + 1):
        page = freq[random.randint(0, len(freq)-1)]
        # print('{}.testing {} on {}...'.format(idx, page, server))
        test(server, session, idx, page)


if __name__ == '__main__':
    # run with different parameters
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for rep in replicas:
            executor.submit(random_test, rep, pageviews, 1)
            # executor.submit(serial_test, rep, pageviews, 1600)
