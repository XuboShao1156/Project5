import socket
import requests


def query(ip) -> (int, int):
    return _query_by_api(ip)


session = requests.session()
def _query_by_api(ip) -> (int, int):
    resp = session.get('https://geolite.info/geoip/v2.1/city/' + ip, auth=('708001', 'RRX49qWHqHjWSrQq'))
    if resp.status_code / 100 != 2:
        raise Exception('ip location query not succeed!')

    body = resp.json()
    return round(body['location']['latitude']), round(body['location']['longitude'])


def _query_by_db(ip) -> (int, int):
    pass


if __name__ == '__main__':
    servers = []
    with open('replica_server', 'r') as f:
        for host in f.readlines():
            host = host.rstrip('\n')
            ip = socket.gethostbyname(host)
            servers.append([host, ip, query(ip)])
    print(servers)
