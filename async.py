import asyncio
import requests

def _try_get(session, url, auth):
    try:
        return session.get(url, auth=auth)
    except:
        return 'failed'


external_session = requests.session()
_try_get(external_session, 'https://geolite.info', None)
async def _query_external_api(ip) -> (int, int):
    resp = await _await_response(external_session, 'https://geolite.info/geoip/v2.1/city/' + ip,
                                 ('708001', 'RRX49qWHqHjWSrQq'))
    if resp == 'failed' or resp.status_code / 100 != 2:
        return 'failed', (0, 0)

    body = resp.json()
    return 'query external api...', round(body['location']['latitude']), round(body['location']['longitude'])


internal_session = requests.session()
_try_get(internal_session, 'http://45.33.89.80:40007/geoip/45.33.89.80', None)
async def _query_internal_api(ip) -> (int, int):
    resp = await _await_response(internal_session, 'http://45.33.89.80:40007/geoip/' + ip, None)
    if resp == 'failed' or resp.status_code / 100 != 2:
        return 'failed', (0, 0)

    body = resp.json()
    return 'query internal api...', round(body['lat']), round(body['lon'])


async def _await_response(session, url, auth):
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, _try_get, session, url, auth)
    return resp


async def _query_api():
    tasks = [asyncio.create_task(_query_internal_api('45.33.89.90')),
             asyncio.create_task(_query_external_api('45.33.89.90'))]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result[0] == 'failed':
            continue
        return result

print(asyncio.run(_query_api()))
