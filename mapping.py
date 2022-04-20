from geo import query
from math import sin, cos, sqrt, atan2, radians

replicas = [['p5-http-a.5700.network', '50.116.41.109', (34, -84)],
            ['p5-http-b.5700.network', '45.33.50.187', (38, -122)],
            ['p5-http-c.5700.network', '194.195.121.150', (-34, 151)],
            ['p5-http-d.5700.network', '172.104.144.157', (50, 9)],
            ['p5-http-e.5700.network', '172.104.110.211', (36, 140)],
            ['p5-http-f.5700.network', '88.80.186.80', (52, 0)],
            ['p5-http-g.5700.network', '172.105.55.115', (19, 73)]]


def map_replica(ip) -> str:
    lat, lon = query(ip)

    best = 0
    min_dist = 1_000_000_000
    for idx, rep in enumerate(replicas):
        dist = _distance(lat, lon, rep[2][0], rep[2][1])
        if dist < min_dist:
            min_dist = dist
            best = idx

    return replicas[best][1]


def _distance(lat1, lon1, lat2, lon2) -> float:
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6373 * c
