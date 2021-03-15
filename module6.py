import os
import sqlite3
import mysql.connector
import sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#数据库

def sqlite3use():
    db_file = os.path.join(os.path.dirname(__file__), 'test.db')
    if os.path.isfile(db_file):
        os.remove(db_file)
    # 初始数据:
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
    cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
    cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
    cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
    cursor.close()
    conn.commit()
    conn.close()
    # 查询 返回指定分数区间的名字，按分数从低到高排序
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # cursor.execute('select * from user where score between ? and ? order by score',(60,68))
    cursor.execute('select * from user where score >= ? and score <= ? order by score', (60, 100))
    result = cursor.fetchall()
    for i in result:
        print(i)


def mysqluse():
    global cursor
    db = mysql.connector.connect(user='root', password='123456', database='roott')
    cursor = db.cursor()
    cursor.execute('create table if not exists user(id varchar(20) primary key,name varchar(20))')
    # cursor.execute('insert into user(id,name) values(%s,%s)',['1','zyh'])
    cursor.close()
    db.commit()
    cursor = db.cursor()
    cursor.execute('select * from user where id = %s', ['1'])
    result = cursor.fetchall()
    for i in result:
        print(i)
    cursor.close()
    db.close()


# step 1 创建对象的基类:
Base = declarative_base()

# step 2 定义User对象:
class User(Base):
    #表的名字
    __tablename__ = 'user'

    #表的结构
    id = Column(String(20),primary_key=True)
    name = Column(String(20))


def sqlalchemyuse():
    # step 3 初始化数据库连接 '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/roott')
    # step 4 创建DBSession类型:DBSession对象可视为当前数据库连接
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # 添加对象到session
    session.add(User(id='2', name='ln'))
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter(User.id == '2').one()
    print(type(user))
    print(user.name)
    # 关闭session
    session.close()


if __name__ == '__main__':

    # sqlite3use()
    # mysqluse()
    #在Python中，最有名的ORM框架是SQLAlchemy
    # sqlalchemyuse()
    pass