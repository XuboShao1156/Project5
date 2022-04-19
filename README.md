# High Level Approach & Implementation
## DNS
For the milestone, since we only have one HTTP server, the dns hardcodes the server's ip in the DNS answer.
Besides, we also made progress on the geo-database.
We currently use [GEO-lite](https://dev.maxmind.com/geoip/docs/databases/city-and-country?lang=en).
However, since the GEO-lite database is too large, we are trying to shrink it by clustering according to geo-location and merging ip addresses within a cluster.
We may also try to use `scamper` later to improve the performance if necessary.
In that case, we will try to probe the HTTP servers every 1 second and answer the client with fastest server within that second.

## HTTP Server
HTTP server takes in http requests from clients and response with the content which clients required.
We implemented the server using [HTTP servers](https://docs.python.org/3/library/http.server.html) module under http.server. It creates and listens at the HTTP socket.
We bind the Ip address to '0.0.0.0' right now so it can bind with all Ip address.
We use requests library to fetch data from origin server if current path is not stored in cache. Since the project is not for HTTP protocol, using librarys makes project succinct. 
Currently we simply using a dictionary as a cache. URL stored as key, contents stored as values. Only if URL is not stored in dictionary we send a request to the origin server. 
We are planning using LRU Algorithm for cache managment. For milestone, we implement it using lru_cache to simulate that. 
 

# Challenges
## DNS
The geo-location database is too large, we are still trying to find a good way to cluster and merge ip address.
## DNS
How to apply LRU Algorithm on caching managment and improve overall efficiency will be tricky because there is a limitation on disk usage.
Maybe using some statistic methodology could improve it such as Bloom Filter. 
