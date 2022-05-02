import csv
import os
import heapq

# The content of pages with higher frequency than MEM_MIN_FREQ will be compressed by gzip and stored in memory.
# According to our analysis script (see statistics.py) and measurements (see size.log),
# the size of compressed content of pages with higher frequency than 1650 is 19.57MB.
MEM_MIN_FREQ = 1650

# limit the disk usage to store content of pages
DISK_LIMIT = 20 * 1000 * 1000

class Cache(object):
    """
    This class implements a two-layer cache for HTML pages:
    1. memory layer: for pages will higher frequency than mem_min_freq, the content will be stored in memory
    2. disk layer: for pages with lower frequency than mem_min_freq, the content will be stored in storage and limited
    by disk_threshold. To avoid exceeding this threshold and maximize the performance, we will replace the least
    frequent page with the new page if it has a higher frequency.
    """
    def __init__(self, mem_min_freq=MEM_MIN_FREQ, disk_threshold=DISK_LIMIT,
                 disk_folder='./pages', freq_file='pageviews.csv'):
        self.mem_min_freq = mem_min_freq
        # minimal frequency requirement to store the page in memory

        self.freq = dict()  # path -> frequency
        with open(freq_file, encoding='utf-8') as f:
            for row in csv.reader(f):
                self.freq[row[0]] = int(row[1])
        # os.remove(freq_file)
        self.mem_cache = dict()  # path -> content in bytes

        self.disk_cache = dict()  # path -> len(content)
        self.disk_queue = []  # queue of pages prioritized by frequency

        self.disk_usage = 0
        self.disk_threshold = disk_threshold  # maximum disk usage

        self.disk_folder = disk_folder  # folder to store pages
        if os.path.exists(disk_folder):
            os.popen('rm -rf ' + disk_folder).read()
        os.mkdir(disk_folder)

        self.mem_size = 0

    def put(self, page: str, content: bytes) -> None:
        if self.freq[page] > self.mem_min_freq:  # store page in memory
            self.mem_cache[page] = content
            self.mem_size += len(content)
        else:  # store page in disk
            # if disk is full and new page has a higher frequency, pop the least frequent item out
            while self.disk_usage + len(content) >= self.disk_threshold \
                    and self.freq[page] > self.freq[self.disk_queue[0][1]]:
                victim_page = heapq.heappop(self.disk_queue)
                os.remove(self.disk_folder + '/' + victim_page[1])
                self.disk_usage -= self.disk_cache[victim_page[1]]
                del self.disk_cache[victim_page[1]]

            # if disk is not full, write the page
            if self.disk_usage + len(content) < self.disk_threshold:
                heapq.heappush(self.disk_queue, (self.freq[page], page))
                with open(self.disk_folder + '/' + page, 'wb') as f:
                    f.write(content)
                self.disk_usage += len(content)
                self.disk_cache[page] = len(content)

    def get(self, page) -> bytes:
        if page in self.mem_cache: # check in memory
            print('fetch page {} from memory...'.format(page))
            return self.mem_cache[page]
        elif page in self.disk_cache: # check in disk
            print('fetch page {} from disk...'.format(page))
            with open(self.disk_folder + '/' + page, 'rb') as f:
                return f.read()
        else: # page not cached
            return b''


# test
if __name__ == '__main__':
    cache = Cache(mem_min_freq=50_000, disk_threshold=27)

    print(cache.get('Main_Page'))
    cache.put('Main_Page', b'main page')
    print(cache.get('Main_Page'))

    print(cache.get('-'))
    cache.put('-', b'----------')
    print(cache.get('-'))

    print(cache.get('Patrick_Mahomes'))
    cache.put('Patrick_Mahomes', b'Patrick Mahomes')
    print(cache.get('Patrick_Mahomes'))

    print(cache.get('Conor_McGregor'))
    cache.put('Conor_McGregor', b'Conor McGregor')
    print(cache.get('Conor_McGregor'))

    print(cache.get('Aaron_Hernandez'))
    cache.put('Aaron_Hernandez', b'Aaron_Hernandez')
    print(cache.get('Aaron_Hernandez'))

    print(cache.get('Coronavirus'))
    cache.put('Coronavirus', b'Coronavirus')
    print(cache.get('Coronavirus'))
