import asyncio
import threading
from aiohttp import web

#异步IO

# yield生产者消费者模式
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()


async def hello():
    print(f'hello word {threading.current_thread()}')
    r = await asyncio.sleep(1)
    print(f'hello zyh  {threading.current_thread()}')


async def wget(host):
    print(f'wget {host}')
    connect = asyncio.open_connection(host,80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


def asynciouse():
    loop = asyncio.get_event_loop()  # 获取EventLoop:
    # tasks = [hello(),hello()]
    # asyncio异步网络连接获取sina、sohu和163的网站首页
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))  # 执行coroutine
    loop.close()


async def index(request):
    await asyncio.sleep(1)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(1)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(lp):
    app = web.Application(loop=lp)
    app.router.add_route('GET','/',index)
    app.router.add_route('GET','/hello/{name}',hello)
    srv = await loop.create_server(app.make_handler(),'127.0.0.1',8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv


if __name__ == '__main__':
    c = consumer()
    # produce(c)

    # asyncio使用
    # asynciouse()

    #asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

    pass
