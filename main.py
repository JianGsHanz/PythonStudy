# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random
import sys
import time

from module1 import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def temperature_transform():
    f = float(input("请输入华氏摄氏度："))
    c = (f - 32) / 1.8
    print("%.1f华氏度 = %.1f摄氏度" % (f, c))
    print(f"{f:.1f}华氏度 = {c:.1f}摄氏度")


def loop_use():
    x = float(input("请输入："))
    if x > 1:
        x = 3 * x - 5
    else:
        if x < -1:
            x = 5 * x + 3
        else:
            x = x + 2
    print('x = %.1f' % x)
    for x in range(1, 100):
        if x % 2 == 0:
            print(x)

    result = random.randint(1, 100)
    count = 0
    while True:
        count += 1
        num = int(input("请输入："))
        if num > result:
            print('猜大了')
        elif num < result:
            print('猜小了')
        else:
            print('恭喜你！')
            break
        if count == 10:
            print('10次都不中，你太笨了')
            break
    print(f'你只用了 {count:d}次就猜到了')


def dataStructure():
    # 创建列表
    list1 = [1, 2, 3, 3, 3, 2]
    list2 = [x for x in range(1, 10)]  # list
    list3 = (x for x in range(1, 10))  # generator生成器
    # 创建集合的字面量语法
    set1 = {1, 2, 3, 3, 3, 2}
    set2 = (range(10))
    set3 = set((1, 2, 3, 3, 2, 1))
    # 创建集合的推导式语法(推导式也可以用于推导集合)
    set4 = {num for num in range(1, 100) if num % 3 == 0 or num % 5 == 0}
    # 向集合添加删除元素
    set1.add(4)
    set1.add(5)
    set1.update([11, 12])
    set1.discard(5)
    if 4 in set1:
        set1.remove(4)
    # 创建元组
    tuple1 = (1, 2, 3, 3, 3, 2)
    # 创建字典
    dict1 = {1: '一', 2: '二', 3: '三', 3: '三', 2: '二', 1: '一'}
    dict2 = dict(zip([1, 2, 3], '一二三'))
    # 创建字典的推导式语法
    dict3 = {num: num ** 2 for num in range(1, 10)}
    print(dict1.get(1))
    print(list1)
    print(sys.getsizeof(list1))
    print(set1)
    print(sys.getsizeof(set1))
    print(tuple1)
    print(sys.getsizeof(tuple1))
    print(dict1)
    print(sys.getsizeof(dict1))
    print(dict2)


def marquee():
    # 在屏幕上显示跑马灯文字
    content = '北京欢迎你...'
    while True:
        os.system('cls')
        print(content)
        # 休眠200毫秒
        time.sleep(0.2)
        content = content[1:] + content[0]


def generate_code(code_len=4):
    # 产生指定长度的验证码，验证码由大小写字母和数字构成。
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    all_chars_len = len(all_chars) - 1
    code = ''
    for _ in range(code_len):
        index = random.randint(0, all_chars_len)
        code += all_chars[index]
    return code


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # temperature_transform()
    # loop_use()
    dataStructure()
    # marquee()
    print(generate_code())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
