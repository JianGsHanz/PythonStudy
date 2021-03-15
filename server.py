from wsgiref.simple_server import make_server
#web服务
'''
除了Flask，常见的Python Web框架还有：

Django：全能型Web框架；

web.py：一个小巧的Web框架；

Bottle：和Flask类似的Web框架；

Tornado：Facebook的开源异步Web框架。
'''
from flask import Flask, request, render_template


def application(environ,start_response):
    start_response('200 ok',[('Content-Type','text/html')])
    body = '<h1>Hello %s!</h1>' % (environ['PATH_INFO'][1:] or 'word')
    return [body.encode('utf-8')]
    # return [b'<h1>Hello Word!</h1>']


def wsgiref_use():
    # 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
    httpd = make_server('', 8000, application)
    print('server HTTP on port 8000...')
    # 开始监听http请求
    httpd.serve_forever()


'''
MVC模式
C：Controller，Controller负责业务逻辑，比如检查用户名是否存在，取出用户信息等等
V：包含变量{{ name }}的模板就是V：View，View负责显示逻辑，通过简单地替换一些变量，View最终输出的就是用户看到的HTML
M：Model是用来传给View的，这样View在替换变量的时候，就可以从Model中取出相应的数据。只是因为Python支持关键字参数，很多Web框架允许传入关键字参数，然后，在框架内部组装出一个dict作为Model
'''
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/signin',methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    username = request.form['username']
    if username == 'admin' and request.form['password'] == 'password':
        return render_template('signin-ok.html',username=username)
    return render_template('form.html',message='Bad username or password', username=username)


if __name__=='__main__':
    #wsgiref使用
    # wsgiref_use()
    # 若不配置host和port，则默认是localhost，端口为5000
    # app.run()

    pass