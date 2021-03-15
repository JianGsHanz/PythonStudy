import socket
from tkinter import messagebox

from PIL import Image, ImageFilter
import requests
import chardet
import psutil
import tkinter
from turtle import *
#常用的三方模块

def imageuse():
    # 打开图片
    im = Image.open('C:/Users/agoto/Desktop/cat.jpg')
    # 获取尺寸
    w, h = im.size
    print(f'图片宽：{im.size[0]}，高：{im.size[1]}')
    # 缩放到50%
    # image.thumbnail((w//2,h//2))
    # 模糊滤镜
    im2 = im.filter(ImageFilter.BLUR)
    # 保存
    im2.save('C:/Users/agoto/Desktop/cat_blur.jpg')


def requestsuse():
    # GET
    re = requests.get('http://www.baidu.com/')
    print(re.status_code)
    print(re.text)
    # requests自动检测编码，可以使用encoding属性查看
    print(re.encoding)
    # 无论响应是文本还是二进制内容，我们都可以用content属性获得bytes对象
    print(re.content)
    # 带参数的URL，传入一个dict作为params参数
    re1 = requests.get('http://www.douban.com/search', params={'q': 'python', 'cat': '1001'})
    print(re1.url)
    # requests的方便之处还在于，对于特定类型的响应，例如JSON，可以直接获取
    re2 = requests.get('http://test2.api.agotoz.net/api/app/devices')
    print(re2.json())
    # 需要传入HTTP Header时，我们传入一个dict作为headers参数
    re3 = requests.get('https://www.douban.com/',
                       headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)'})
    # POST
    # requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数
    requests.post('', json={'key': 'value'})  # 内部自动序列化为JSON
    # 上传文件需要更复杂的编码格式，但是requests把它简化成files参数
    upload_files = {'file': open('report.xls', 'rb')}
    repost = requests.post('', files=upload_files)
    # requests对Cookie做了特殊处理，使得我们不必解析Cookie就可以轻松获取指定的Cookie
    repost.cookies['ts']
    # 在请求中传入Cookie，只需准备一个dict传入cookies参数
    cs = {'token': '12345', 'status': 'working'}
    requests.get('url', cookies=cs)
    # 要指定超时，传入以秒为单位的timeout参数
    requests.get('', timeout=2.5)


def psutiluse():
    print(psutil.cpu_count())  # CPU逻辑数量
    print(psutil.cpu_count(logical=False))  # CPU物理核心
    print(psutil.cpu_times())  # 统计CPU的用户／系统／空闲时间
    # 实现类似top命令的CPU使用率，每秒刷新一次，累计10次
    for x in range(10):
        print(psutil.cpu_percent(interval=1, percpu=True))


class Application(tkinter.Frame):
    # Python支持多种图形界面的第三方库，包括：Tk、wxWidgets、Qt、GTK等等
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        #pack()方法把Widget加入到父容器中，并实现布局，pack()是最简单的布局，grid()可以实现更复杂的布局
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = tkinter.Label(self,text='hello word')
        #pack()方法把Widget加入到父容器中，并实现布局，pack()是最简单的布局，grid()可以实现更复杂的布局
        self.helloLabel.pack()
        #当Button被点击时，触发self.quit()使程序退出
        self.quitButton = tkinter.Button(self,text='Quit',command=self.quit)
        #pack()方法把Widget加入到父容器中，并实现布局，pack()是最简单的布局，grid()可以实现更复杂的布局
        self.quitButton.pack()


def tkuse():
    # 在GUI中，每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。
    app = Application()
    # 设置窗口标题:
    app.master.title('hello')
    # 主消息循环:
    app.mainloop()


class Application1(tkinter.Frame):
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = tkinter.Entry(self)
        self.nameInput.pack()
        self.alterButton = tkinter.Button(self,text='click',command=self.hello)
        self.alterButton.pack()
        pass

    def hello(self):
        name = self.nameInput.get() or 'word'
        messagebox.showinfo('Message',f'Hello {name}',command=self.quit)
        pass


def tkinputuse():
    app = Application1()
    app.master.title('zyh')
    app.mainloop()


def rectangleuse():
    # 绘制矩形
    # 设置笔刷宽度
    width(4)
    # 前进
    forward(100)
    # 笔刷颜色
    pencolor('yellow')
    # 右转90度
    right(90)
    forward(100)
    pencolor('red')
    right(90)
    forward(100)
    pencolor('blue')
    right(90)
    forward(100)
    # 调用done()使得窗口等待被关闭，否则将立刻关闭窗口:
    done()

def drawStar(x, y):
    pu()
    goto(x, y)
    pd()
    # set heading: 0
    seth(0)
    for i in range(5):
        fd(40)
        rt(144)


def clientsocketuse():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.sina.com.cn', 80))
    # 发送数据:
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    # 接收数据:
    buffer = []
    while True:
        # 每次最多接收1k字节:接收数据时，调用recv(max)方法，一次最多接收指定的字节数，因此，在一个while循环中反复接收，直到recv()返回空数据，表示接收完毕，退出循环。
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    #接收完数据后，调用close()方法关闭Socket，这样，一次完整的网络通信就结束了
    s.close()
    #收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件
    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))
    # 把接收的数据写入文件:
    with open('sina.html', 'wb') as f:
        f.write(html)


if __name__ == '__main__':
    # 图片使用
    # imageuse()
    # requests用于网络，相比urllib更实用高级
    # requestsuse()

    # 检测字符编码
    # print(chardet.detect('离离原上草，一岁一枯荣'.encode('gbk')))
    # print(chardet.detect('离离原上草，一岁一枯荣'.encode('utf-8')))

    #psutil获取系统信息
    # psutiluse()

    #GUI图形界面
    # tkuse()
    # tkinputuse()

    #turtle绘图应用
    # rectangleuse()
    # for x in range(0, 250, 50):
    #     drawStar(x, 0)

    #Socket
    # clientsocketuse()

    pass
