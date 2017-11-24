import aiohttp
import asyncio
import urllib.parse

import time


class BoundedDomain:
    def __init__(self,
                 domain: str,
                 concurrency_size: int=1,
                 seconds: int=1,
                 minutes: int=None):
        self.domain = domain
        self.concurrency_size = concurrency_size
        self.seconds = seconds
        self.minutes = minutes
        self.bucket = asyncio.Queue()

        self.bucket_refreshed_per_second = asyncio.Queue()
        self.last_refreshed_second = None
        self.bucket_refreshed_per_minute = asyncio.Queue()
        self.last_refreshed_minute = None


class DomainThrottle:
    """
    Throttling by token bucket algorithm.
    """
    def __init__(self, rate):
        self._consume_lock = asyncio.Lock()
        self.rate = rate
        self.last = 0
        self.tokens = 0

    async def consume(self, amount=1):
        async with self._consume_lock:
            now = time.time()

            if self.last == 0:
                self.last = now

            elapsed = now - self.last

            if int(elapsed * self.rate):
                self.tokens += int(elapsed * self.rate)
                self.last = now

            self.tokens = (
                self.rate
                if self.tokens > self.rate
                else self.tokens
            )

            if self.tokens >= amount:
                self.tokens -= amount
            else:
                amount = 0

            return amount

    async def __aenter__(self, url):
        hostname = urllib.parse.urlparse(url).hostname
        print('entering context')

    async def __aexit__(self, exc_type, exc, tb):
        print('exiting context')


def worker(work_queue, results_queue, throttle):
    while True:
        try:
            item = work_queue.get(block=False)
        except asyncio.QueueEmpty:
            break
        else:
            while not throttle.consume():
                pass

            try:
                result = fetch_place(item)
            except Exception as err:
                results_queue.put(err)
            else:
                results_queue.put(result)
            finally:
                work_queue.task_done()


async def fetch(l, url):
    async with aiohttp.ClientSession(loop=l) as session:
        async with session.get(url) as response:
            return await response.text()


async def bound_fetch(semaphore, l, url):
    async with DomainThrottle(3):
        async with semaphore:
            return await fetch(l, url)


async def main(l, url, num):
    s = asyncio.Semaphore(3)
    tasks = [bound_fetch(s, l, url) for _ in range(num)]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(loop, 'http://localhost:8000', 9))
    for r in results:
        print(r)
