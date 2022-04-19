# High Level Approach & Implementation
## DNS
For the milestone, since we only have one HTTP server, the dns hardcodes the server's ip in the DNS answer.
Besides, we also made progress on the geo-database.
We currently use [GEO-lite](https://dev.maxmind.com/geoip/docs/databases/city-and-country?lang=en).
However, since the GEO-lite database is too large, we are trying to shrink it by clustering according to geo-location and merging ip addresses within a cluster.
We may also try to use `scamper` later to improve the performance if necessary.
In that case, we will try to probe the HTTP servers every 1 second and answer the client with fastest server within that second.

## HTTP Server

# Challenges
## DNS
The geo-location database is too large, we are still trying to find a good way to cluster and merge ip address.

