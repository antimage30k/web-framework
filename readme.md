# 基于 Socket 和 HTTP 的 Web MVC 框架

**简介**
-
- 使用 `Socket` 进行通信，构建完整的 `Web Server`，使用多线程实现并发访问。
- `MVC` 架构，耦合度低、重用度高。
- `Mode`l 层基于 `MySQL` 实现 `ORM`，实现对不同类型数据的 `CRUD`；同时支持数据库事务，支持 `JOIN` 子句的 `SQL` 语句拼接，能解决 `ORM` `N+1` 问题。
- `View` 层使用 `Jinja` 模板，简化网页生成。
- `Controller` 层为自制 `Web` 框架，实现了路由注册、路由分发、解析 `HTTP` 请求和生成 `HTTP` 响应等功能。
- 实现用户注册与登录，用 `Session` 实现用户身份识别，实现了用户权限管理。
- 实现了用户留言及评论功能，并对用户输入进行转义以防御 `XSS` 攻击。



**功能演示**
-
- 注册与登录
![register&login.gif](https://i.loli.net/2019/07/14/5d2ac5391870560571.gif)

- 微博与评论
![weibo&comment.gif](https://i.loli.net/2019/07/14/5d2ac5387e63c59927.gif)

- 防御 `XSS` 攻击
![xss-defense.gif](https://i.loli.net/2019/07/14/5d2ac53fec1a536224.gif)

- 留言
![message-ajax.gif](https://i.loli.net/2019/07/16/5d2cbff8e9fcf28504.gif)

- 查看所有评论过的微博
![all-comments.gif](https://i.loli.net/2019/07/14/5d2ac535df65c57772.gif)

- 管理员修改用户密码
![change-password.gif](https://i.loli.net/2019/07/14/5d2ac539c6fc628772.gif)



**依赖**
-
- `Python 3.6`
- `MySQL`
- `Jinja2`
- `PyMySQL`

**如何运行**
-
- 您需要在根目录下添加 `secret.py` 文件，内容为：
    ```python
    mysql_password = '您的 MySQL 密码'
    ```

- 运行 `db_reset.py`

- 运行 `server.py`