import codecs
import json
from log_util import log
import os
try:
    import pickle
except ImportError:
    import cProfile as pickle
#IO编程

def search(s):
    for x in os.listdir('.'):
        if (os.path.isfile(x) or os.path.isdir(x)) and s in os.path.splitext(x)[0]:
            print(x)


def read_file():
    try:
        f = open('C:/Users/agoto/Desktop/log.txt')
        log(f.read())
    finally:
        if f:
            f.close()
    # Python引入了with语句来自动帮我们调用close()方法
    # 标示符'r'表示读,读取二进制文件，比如图片、视频等等，用'rb'模式打开
    with open('C:/Users/agoto/Desktop/log.txt','r') as f:
        print(f.read(100))
    for line in f.readlines():
        print(line.strip())
    # codecs模块帮我们在读文件时自动转换编码，直接读出unicode
    with codecs.open('C:/Users/agoto/Desktop/test.log','r','gbk') as f:
        print(f.read())


def write_file():
    ''' 写文件
        写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件
    '''
    with codecs.open('C:/Users/agoto/Desktop/log.txt','w') as f:
        f.write('Hello, world!')


def operating_dir():
    # 系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
    print(os.name)
    # 环境变量
    print(os.environ)
    # 获取某个环境变量值
    print(os.getenv('path'))
    # 操作文件和目录
    print(os.path.abspath('.'))
    # 在某个目录下创建一个新目录，
    # 首先把新目录的完整路径表示出来:
    # 两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符
    # 同样的道理，要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数
    print(os.path.join(os.path.abspath('.'), 'testdir'))
    # 然后创建一个目录:
    if not os.path.lexists(os.path.join(os.path.abspath('.'), 'testdir')):
        os.mkdir(os.path.join(os.path.abspath('.'), 'testdir'))
    # 删掉一个目录:
    os.rmdir(os.path.join(os.path.abspath('.'), 'testdir'))
    # os.path.splitext可以直接得到文件后缀
    print(os.path.splitext('C:/Users/agoto/Desktop/test.log')[1])
    # os.rename('C:/Users/agoto/Desktop/test.log','C:/Users/agoto/Desktop/testq.log')
    # os.remove('C:/Users/agoto/Desktop/testq.log')
    print('列出当前目录下的所有目录')
    for x in os.listdir('.'):
        if os.path.isdir(x):
            print(x)
    print([x for x in os.listdir('.') if os.path.isdir(x)])
    print('列出当前目录下的所有py文件')
    print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py'])
    print('在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件或目录')
    search('v')

class Student(object):
    def __init__(self,name,age):
        self._name = name
        self._age = age

# 转换函数
def student2dict(self):
    return {'name': self._name,'age':self._age}

def dict2student(s):
    return Student(s['name'],s['age'])


def serialization():
    # 尝试把一个对象序列化并写入文件
    filename = 'C:/Users/agoto/Desktop/log.txt'
    d = dict(name='zyh', age=20, gender='男')
    with open(filename, 'wb') as f:
        pickle.dump(d, f)
    with open(filename, 'rb') as f:
        print(pickle.load(f))
    d = {'name': 'tom', 'age': 20, 'interest': ['music', 'movie']}
    # json 序列化字典
    print(json.dumps(d))
    print(json.loads(json.dumps(d)))
    #json 对象序列化json
    s = Student('zyh', 18)
    #通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量。也有少数例外，比如定义了__slots__的class。
    # print(json.dumps(s,default=lambda obj: obj.__dict__))
    #自定义转换函数
    print(json.dumps(s,default=student2dict))

    #json反序列化对象
    json_str = '{"age": 20, "name": "zyh"}'
    print(json.loads(json_str,object_hook=dict2student))


#文件读写&操作文件和目录
if __name__ == '__main__':
    # '读文件'
    # read_file()
    #写文件
    # write_file()
    #操作目录
    # operating_dir()
    #序列化操作
    serialization()


