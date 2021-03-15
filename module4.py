import os
import random
import re
import subprocess
import threading
import time
from datetime import datetime
from html.parser import HTMLParser
from multiprocessing.dummy import Process, Pool
from urllib import request,robotparser
#进程线程网络

def run_child_process(name):
    print(f'Run child process {name} ({os.getpid()})..')


def multiprocessing():
    # 启动一个子进程并等待其结束
    print('Parent process %s.' % os.getpid())
    # 创建子进程时，只需要传入一个执行函数和函数的参数
    p = Process(target=run_child_process, args=('子进程',))
    print('Process start')
    p.start()
    # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    p.join()
    print('Process end.')


def long_time_task(name):
    print(f'Run child process {name} ({os.getpid()}).. \n')
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f'Task {name} runtime:{end - start} \n')


def pooluse():
    # Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了
    print('Parent process %s.' % os.getpid())
    pool = Pool()
    for i in range(5):
        pool.apply_async(long_time_task, args=(i,))
    print('Process Start.')
    pool.close()
    pool.join()
    print('Process end.')


def subprocessuse():
    print('$ nslookup www.baidu.com')
    r = subprocess.call(['nslookup', 'www.baidu.com'])
    print(f'Exit code:{r}')
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 如果子进程还需要输入，则可以通过communicate()方法输入
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('gbk'))
    print('Exit code:', p.returncode)


def loope():
    print(f'thread {threading.current_thread().name} is running..')
    n = 0
    while n < 5:
        n += 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s end.' % threading.current_thread().name)


def threadinguse():
    print(f'Thread {threading.current_thread().name} running.')
    t = threading.Thread(target=loope, name='LooperThread')
    t.start()
    t.join()
    print(f'Thread {threading.current_thread().name} end.')


# 假定这是你的银行存款:
balance = 0
lock = threading.Lock()


def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    #同步
    for i in range(2000000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()


def lockuse():
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


def urllibuse():
    req = request.Request('http://www.douban.com/')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 FS')
    with request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        # for k, v in f.getheaders():
        #     print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))


def htmlparseruse():
    myParser = MyHTMLParser()
    myParser.feed('''
    <html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>
    ''')


if __name__ == "__main__":
    # 多进程
    # multiprocessing()
    # Pool 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
    # pooluse()
    # subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出
    # subprocessuse()

    # threading 创建子线程
    # threadinguse()
    #Lock 同步锁
    # lockuse()

    #urlLib GET请求
    # urllibuse()
    parser = robotparser.RobotFileParser()
    parser.set_url('https://www.taobao.com/robots.txt')
    parser.read()
    print(parser.can_fetch('*', 'http://www.taobao.com/article'))
    #HTMLparser
    # htmlparseruse()

