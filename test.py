import asyncio

import etcd3_asyncio as etcd3


async def main():
    async for e in etcd3.Watch(b'/devices/'):
        print(e)


async def locker(n):
    lock = etcd3.Lock('a')
    async with lock:
        print(n, 'locked')
    print(n, 'released')


async def conditioner(n):
    cond = etcd3.Condition('a')
    async with cond:
        while True:
            get = etcd3.Get('a', default=0)
            r = await cond.wait(get)
            if int(r[0]) == n:
                await etcd3.Put('a', n+1)
                cond.notify_all()
                print(n, '->', n+1)
                break


async def notifier():
    cond = etcd3.Condition('a')
    await asyncio.sleep(5)
    cond.notify_all()

asyncio.get_event_loop().create_task(main())

for n in range(0):
    asyncio.get_event_loop().create_task(locker(n))
for n in range(0):
    asyncio.get_event_loop().create_task(conditioner(99-n))
asyncio.get_event_loop().create_task(notifier())

asyncio.get_event_loop().run_forever()
