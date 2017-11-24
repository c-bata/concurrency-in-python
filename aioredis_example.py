import asyncio
import aioredis

async def connection_example(key):
    conn = await aioredis.create_connection('/tmp/redis.sock')
    return await conn.execute('GET', key)


async def main(num):
    tasks = [connection_example('my-key') for _ in range(num)]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(3))
    for r in results:
        print(r)
