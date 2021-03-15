from abc import ABCMeta, abstractmethod
from log_util import log
#多态多继承
# 交通工具 (利用ABCMeta和@abstractmethod来抽象一个类)
class Transportation(object, metaclass=ABCMeta):
    __slots__ = ()

    def carry_passengers(self):
        print('载客')

    @abstractmethod
    def get_passenger_info(self):
        pass


# 飞行能力 Mixin的目的就是给一个类增加多个功能
class FlyMixin(object):
    __slots__ = ()

    def fly(self):
        print('飞行')


# 飞机
class Aeroplane(Transportation, FlyMixin):
    # 当你事先知道class的attributes的时候，建议使用slots来节省memory以及获得更快的attribute access。
    # 如果你想获得__slots__的好处并且可以创造新的attribute，你可以将__dict__作为__slots__中的一个element
    __slots__ = 'name', 'age', '__dict__'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_passenger_info(self):
        print(f'现在乘客为{self.name},年龄：{self.age}')


# 高铁
class HighSpeedRail(Transportation):

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    def get_passenger_info(self):
        print(f'高铁乘客{self._name},年龄：{self._age}')

    def __str__(self):
        return f'name = {self._name},age = {self._age}'


class Test(object):
    # 静态函数 *args可变参数  **kwargs 关键字参数(dict key-value)
    def __new__(cls, *args, **kwargs):
        print(cls)
        return super().__new__(cls)

    def __init__(self):
        print(self)
        self.name = 'dfdf'

    def person(self, name, age, **kw):
        print('name:', name, 'age:', age, kw)

    def tryUse(self):
        try:
            log('try')
            r = 10 / 0
            log(f'result = {r}')
        except ZeroDivisionError as e:
            log(f'except =  {e}')
        finally:
            log('finally')
        log('end')


if __name__ == '__main__':
    aeroplane = Aeroplane('zyh', 18)
    aeroplane.carry_passengers()
    aeroplane.fly()
    aeroplane.get_passenger_info()
    highSpeedRail = HighSpeedRail('ddd', 11)
    highSpeedRail.get_passenger_info()
    print(f'获取HighSpeedRail类型：{type(highSpeedRail)}')
    # 获得一个对象的所有属性和方法
    print(f'获取HighSpeedRail的所有属性和方法：{dir(highSpeedRail)}')
    test = Test()
    print(f'获取属性name，如果不存在，返回默认值404：{getattr(test, "name", 404)}')
    print(f'有没有属性name：{hasattr(test, "name")}')
    print(f'设置属性age：{setattr(test, "age", 16)}')
    print(f'有没有属性age：{hasattr(test, "age")}')
    print(f'test = {test.name}')

    test.person('z', 1)

    dicts = {'z': '1', 'y': '2', 'h': '3'}
    print({k + '= ' + v for k, v in dicts.items()})
    L = ['Hello', 'World', 'IBM', 'Apple']
    print([i.upper() for i in L])

    test.tryUse()
