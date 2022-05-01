# High Level Approach & Implementation
## DNS
For the milestone, since we only have one HTTP server, the dns hardcodes the server's ip in the DNS answer.
Besides, we also made progress on the geo-database.
We currently use [GEO-lite](https://dev.maxmind.com/geoip/docs/databases/city-and-country?lang=en).
However, since the GEO-lite database is too large, we are trying to shrink it by clustering according to geo-location and merging ip addresses within a cluster.
We may also try to use `scamper` later to improve the performance if necessary.
In that case, we will try to probe the HTTP servers every 1 second and answer the client with fastest server within that second.

## HTTP Server
1.HTTP server takes in http requests from clients and response with the content which clients required.
2.We implemented the server using [HTTP servers](https://docs.python.org/3/library/http.server.html) module under http.server. It creates and listens at the HTTP socket.
3.We bind the Ip address to '0.0.0.0' right now so it can bind with all Ip address.
4.We use requests library to fetch data from origin server if current path is not stored in cache. Since the project is not for HTTP protocol, using librarys makes project succinct. 
5.Based on frequencies from pageview.csv file, we develop a cache system based on LFU (Least Frequency Used) Algorithm. Because we have a disk usage limit and a RSS limit. We store contents with higher frequency in memory and store the lower ones as files in the disk. It could save time from I/O operations.

 

# Challenges
## DNS
The geo-location database is too large, we are still trying to find a good way to cluster and merge ip address.
## HTTP
How to apply LRU Algorithm on caching managment and improve overall efficiency will be tricky because there is a limitation on disk usage.
Maybe using some statistic methodology could improve it such as Bloom Filter. 

# REPORT
## Design Decision
## Effectiveness
## Further Development
