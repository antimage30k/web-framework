import pymysql

import secret
import config
from models.base_model import SQLModel
from models.comment import Comment
from models.message import Message
from models.test_model import Test
from models.session import Session
from models.todo import Todo
from models.user import User, UserRole
# from models.weibo import Weibo
# from models.comment import Comment
from models.weibo import Weibo


def recreate_table(cursor):
    cursor.execute(Test.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    # 执行weibo表的创建
    cursor.execute(Weibo.sql_create)
    # 执行comment的创建
    cursor.execute(Comment.sql_create)
    cursor.execute(Todo.sql_create)
    cursor.execute(Message.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'DROP DATABASE IF EXISTS `{}`'.format(
                    config.db_name
                )
            )
            cursor.execute(
                'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                    config.db_name
                )
            )
            cursor.execute('USE `{}`'.format(config.db_name))

            recreate_table(cursor)

        connection.commit()
    finally:
        connection.close()


def test_data():
    SQLModel.init_db()

    Test.new({})

    form = dict(
        username='test',
        password='1234',
        role=UserRole.normal,
    )
    form_admin = dict(
        username='admin',
        password='123',
        role=UserRole.admin,
    )
    u, result = User.register(form)

    Session.add(u.id)
    User.register(form_admin)

    # form = dict(
    #     content='test weibo',
    # )
    # w = Weibo.add(form, u.id)
    # form = dict(
    #     content='test comment',
    #     weibo_id=w.id,
    # )
    # Weibo.comment_add(form, u.id)

    # SQLModel.connection.close()


# 测试comment
def test_comment():
    form = dict(
        user_id=1,
        weibo_id=1,
        content='Happy Birthday!',
    )
    Comment.new(form)


# 测试weibo类
def test_weibo():
    form = dict(
        user_id=1,
        content='WELCOME! My 10th Birthday!'
    )
    Weibo.new(form)


def test_one(**kwargs):
    m = User.one(**kwargs)
    print(m)


def test_all(**kwargs):
    m = User.all(**kwargs)
    print(m)


if __name__ == '__main__':
    recreate_database()
    test_data()
    # test_one(username='bell', role='normal')
    # test_all(role='normal')
    # test_all()
    test_comment()
    # 运行测试
    test_weibo()
