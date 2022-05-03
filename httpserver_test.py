import concurrent.futures
import csv
import gzip
import random
import time
import requests

replicas = [
    'p5-http-a.5700.network',
    'p5-http-b.5700.network',
    'p5-http-c.5700.network',
    'p5-http-d.5700.network',
    'p5-http-e.5700.network',
    'p5-http-f.5700.network',
    'p5-http-g.5700.network',
    # 'localhost'
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
    start = time.time()
    session = requests.session()
    for idx in range(1, size + 1):
        page = freq[random.randint(0, len(freq)-1)]
        # print('{}.testing {} on {}...'.format(idx, page, server))
        test(server, session, idx, page)
    print('finished random test on replica {} in {}'.format(server, time.time() - start))


def content_test(replica, origin, freq):
    replica_session = requests.session()
    origin_session = requests.session()
    for item in freq:
        p = item[0]
        print('testing page {}...'.format(p))
        replica_resp = replica_session.get('http://{}:40007/{}'.format(replica, p))
        origin_resp = origin_session.get('http://{}:8080/{}'.format(origin, p))

        assert replica_resp.status_code == origin_resp.status_code
        assert replica_resp.content == origin_resp.content

        start = time.time()
        compressed = gzip.compress(replica_resp.content)
        print('compress costs {} for page of size {}'.format(time.time() - start, len(replica_resp.content)))

        start = time.time()
        gzip.decompress(compressed)
        print('decompress costs {} for page of size {}'.format(time.time() - start, len(replica_resp.content)))


if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    #     for rep in replicas:
    #         executor.submit(serial_test, rep, pageviews, 0)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    #     for rep in replicas:
    #         executor.submit(random_test, rep, pageviews, 200)

    content_test(replicas[0], 'cs5700cdnorigin.ccs.neu.edu', pageviews[:50])