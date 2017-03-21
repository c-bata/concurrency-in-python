import aiohttp
import asyncio

async def fetch(l, url):
    async with aiohttp.ClientSession(loop=l) as session:
        async with session.get(url) as response:
            return await response.text()


async def bound_fetch(semaphore, l, url):
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
