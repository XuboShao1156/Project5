import asyncio
import csv
import ipaddress
import time
import requests

# query the geo location of given ip
def query(ip) -> (int, int):
    lat, lon = _query_by_db(ip)
    if lat is None or lon is None:
        ret, lat, lon = asyncio.run(_query_api(ip))
        if ret == 'failed':
            return None, None
        # print(ret)
    return lat, lon

# read the local geo database
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

# query local geo database
def _query_by_db(ip, mask=mask) -> (int, int):
    # print('query db...')
    ip = int(ipaddress.ip_address(ip))
    while ip != 0:
        ip &= mask
        if ip in db:
            return db[ip][1], db[ip][2]
        mask <<= 1
    return None, None

# try get a url
def _try_get(session, url, auth):
    try:
        return session.get(url, auth=auth)
    except:
        return 'failed'


# query external geo web-service
external_session = requests.Session()
_try_get(external_session, 'https://geolite.info', None)
async def _query_external_api(ip) -> (str, int):
    resp = await _await_response(external_session, 'https://geolite.info/geoip/v2.1/city/' + ip,
                                 ('708001', 'RRX49qWHqHjWSrQq'))
    if resp == 'failed' or resp.status_code / 100 != 2:
        return 'failed', (0, 0)

    body = resp.json()
    return 'query external api...', round(body['location']['latitude']), round(body['location']['longitude'])


# query internal geo web-service on Linode
internal_session = requests.Session()
_try_get(internal_session, 'http://45.33.89.80:40007/geoip/45.33.89.80', None)
async def _query_internal_api(ip) -> (str, int, int):
    resp = await _await_response(internal_session, 'http://45.33.89.80:40007/geoip/' + ip, None)
    if resp == 'failed' or resp.status_code / 100 != 2:
        return 'failed', (0, 0)

    body = resp.json()
    return 'query internal api...', round(body['lat']), round(body['lon'])


async def _await_response(session, url, auth):
    resp = await asyncio.get_event_loop().run_in_executor(None, _try_get, session, url, auth)
    return resp


# query multiple geo web-service concurrently and return the first response
async def _query_api(ip):
    # print('query api...')
    for coro in asyncio.as_completed([asyncio.create_task(_query_internal_api(ip)),
                                      asyncio.create_task(_query_external_api(ip))]):
        result = await coro
        if result[0] == 'failed':
            continue
        return result

    return 'failed', 0, 0


if __name__ == '__main__':
    start = time.time()
    print(query('72.74.225.130'))
    print(time.time() - start)
