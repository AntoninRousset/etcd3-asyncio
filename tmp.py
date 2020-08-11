import asyncio
import etcd3_asyncio as etcd3

c = etcd3.Client()


async def main():
    await c.Put(b'a', b'2').send()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
