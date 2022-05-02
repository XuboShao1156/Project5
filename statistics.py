# This script measures how large the most frequent pages are.
# The measurement will be used to help our tweak the memory usage in cache.

import csv
import gzip
import requests

HOST = 'http://cs5700cdnorigin.ccs.neu.edu'
PORT = 8080

# download page and return size of content
session = requests.session()
def download(path) -> bytes:
    resp = session.get('{}:{}/{}'.format(HOST, PORT, path))
    if resp.status_code / 100 != 2:
        print('Code {} for path {}!'.format(resp.status_code, path))

    with open('pages/{}.html'.format(path), 'w') as f:
        f.write(resp.content.decode('utf-8'))

    return resp.content


if __name__ == '__main__':
    logger = open('size.log', 'w')

    total = 0
    gzip_total = 0
    with open('pageviews.csv', 'r') as f:
        cnt = 1
        for row in csv.reader(f):
            content = download(row[0])

            curr = len(content)
            total += curr

            gzip_curr = len(gzip.compress(content))
            gzip_total += gzip_curr

            log = '{}. total size:{}, gzip total:{}, curr size:{}, gzip curr:{}, curr path:{}, curr freq:{}\n'.format(
                cnt, total, gzip_total, curr, gzip_curr, row[0], row[1])
            print(log, end='')
            logger.write(log)

            cnt += 1
            if gzip_total >= 50_000_000: # 50MB is enough for us to analyze since we only need at most 40MB of them
                break

    logger.close()
