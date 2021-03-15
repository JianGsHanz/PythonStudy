# 创建和使用对象
from abc import ABCMeta, abstractmethod
from time import sleep, localtime, time
from types import MethodType


# (object)继承
class Person(object, metaclass=ABCMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def eat(self):
        print("吃饭")


# (Person)继承
class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.name = name
        self.__age = age

    # 访问器
    @property
    def age(self):
        return self.__age

    # 修改器
    @age.setter
    def age(self, age):
        self.__age = age

    def test_something(self):
        print(f"test-something...{self.name}")

    def study(self, course_name):
        print('%s正在学习%s' % (self.name, course_name))
        self.__think(course_name)

    # 在python中属性和方法的访问权限只有两种，公开和私有，私有用两个下滑线开始
    def __think(self, thing):
        print('%s正在想%s %s' % (self.name, thing, self.__age))

    def eat(self):
        print(f"{self.name} 吃饭中")


# 数字时钟
class Clock(object):

    def __init__(self, hour=0, minute=0, second=0):
        self._hour = hour
        self._minute = minute
        self._second = second

    def run(self):
        self._second += 1
        if self._second == 60:
            self._second = 0
            self._minute += 1
            if self._minute == 60:
                self._minute = 0
                self._hour += 1
                if self._hour == 24:
                    self._hour = 0

    def show(self):
        print('%02d:%02d:%02d' % (self._hour, self._minute, self._second))

    @classmethod
    def now(cls):  # cls自定义的 代表当前对象 return对象构造
        ctime = localtime(time())
        return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)


'''
Python是动态语言，可以动态设置属性及方法，设置方法
    stu1 = Student("zyh", 12)
    stu1.address = 'hd' 设置属性
    print(stu1.address)
    stu1.set_name = MethodType(set_name,stu1) 划重点，设置方法
    stu1.set_name('llll')
    print(stu1.name)
给一个实例绑定的方法，对另一个实例是不起作用的，
为了给所有实例都绑定方法，可以给class绑定方法
    Student.address = 'hd'
'''


def set_name(self, name):
    self.name = name


if __name__ == '__main__':
    # stu1 = Student("zyh", 12)
    # Student.address = 'hd'
    # stu1.set_name = MethodType(set_name, stu1)
    # stu1.set_name('llll')
    # print(stu1.name)
    # stu1.test_something()
    # stu1.study("python")
    # print(stu1.age)
    # stu2 = Student('zzz',11)
    # print(f'stu2 = {stu2.address}')
    stu1 = Student('zzyh', 12)
    stu1.eat()
    # 时钟
    # clock = Clock.now()
    # while True:
    #     print(clock.show())
    #     sleep(1)
    #     clock.run()
