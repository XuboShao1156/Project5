import csv
import ipaddress
import time
import requests

def query(ip) -> (int, int):
    lat, lon = _query_by_db(ip)
    if lat is None or lon is None:
        lat, lon = _query_external_api(ip)
    return lat, lon


def _build_geo_db():
    d = dict()
    with open('geo_db.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ip_int = int(ipaddress.ip_address(row['network'].split('/')[0]))
            d[ip_int] = (row['network'], int(row['latitude']), int(row['longitude']))
    return d


db = _build_geo_db()
mask = 0x1
for i in range(32):
    mask = mask << 1 | 0x1
def _query_by_db(ip, mask=mask) -> (int, int):
    print('query db...')
    ip = int(ipaddress.ip_address(ip))
    while ip != 0:
        ip &= mask
        if ip in db:
            return db[ip][1], db[ip][2]
        mask <<= 1
    return None, None


external_session = requests.session()
external_session.get('https://geolite.info')
def _query_external_api(ip) -> (int, int):
    resp = external_session.get('https://geolite.info/geoip/v2.1/city/' + ip, auth=('708001', 'RRX49qWHqHjWSrQq'))
    if resp.status_code / 100 != 2:
        raise Exception('ip location query not succeed!')

    body = resp.json()
    print('query external api...')
    return round(body['location']['latitude']), round(body['location']['longitude'])


internal_session = requests.session()
requests.get('http://45.33.89.80:40007/geoip/45.33.89.80')
def _query_internal_api(ip) -> (int, int):
    resp = internal_session.get('http://45.33.89.80:40007/geoip/' + ip)
    if resp.status_code / 100 != 2:
        raise Exception('ip location query not succeed!')

    body = resp.json()
    print('query internal api...')
    return round(body['lat']), round(body['lon'])


if __name__ == '__main__':
    start = time.time()
    print('query by db: ' + str(_query_by_db('54.251.196.47')))
    print(time.time() - start)

    start = time.time()
    print('query by api: ' + str(_query_by_api('54.251.196.47')))
    print(time.time() - start)
