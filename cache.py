import csv
import os
import heapq

MEM_MIN_FREQ = 5000

# cache for html pages
class Cache(object):
    def __init__(self, mem_min_freq=MEM_MIN_FREQ, disk_threshold=18_000_000, disk_folder='./pages',
                 freq_file='pageviews.csv'):
        self.mem_min_freq = mem_min_freq  # minimal frequency requirement to store the page in memory

        self.freq = dict()  # page -> frequency
        with open(freq_file) as f:
            for row in csv.reader(f):
                self.freq[row[0]] = int(row[1])

        self.mem_cache = dict()     # page -> content in bytes

        self.disk_cache = dict()    # page -> len(content)
        self.disk_queue = []        # queue of pages prioritized by frequency

        self.disk_usage = 0
        self.disk_threshold = disk_threshold    # maximum disk usage

        self.disk_folder = disk_folder  # folder to store pages
        if os.path.exists(disk_folder):
            os.popen('rm -rf ' + disk_folder).read()
        os.mkdir(disk_folder)

    def put(self, page: str, content: bytes) -> None:
        if self.freq[page] > self.mem_min_freq:  # store page in memory
            self.mem_cache[page] = content
        else:  # store page in disk
            # if disk is full and new page has a higher frequency, pop the least frequent item out
            while self.disk_usage + len(content) >= self.disk_threshold and self.freq[page] > self.freq[self.disk_queue[0][1]]:
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
        if page in self.mem_cache:
            return self.mem_cache[page]
        elif page in self.disk_cache:
            with open(self.disk_folder + '/' + page, 'rb') as f:
                return f.read()
        else:
            return b''


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
