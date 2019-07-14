# 基于Socket和HTTP的Web MVC框架

**简介**
-
- 实现基于socket的web框架，编写函数解析HTTP请求，构建HTTP响应；
- MVC架构，耦合度低、重用度高；
- 基于MySQL的SQL语句实现了ORM，基于ORM实现了对用户数据的CRUD；
- 参数化用户输入以避免SQL注入；支持数据库事务，支持join，能解决数据库查询N+1问题；
- 实现用户注册与登录，用cookie和session来识别用户身份；建立了用户权限管理功能；
- 实现了用户留言及评论功能，并对用户输入进行转义以防御XSS攻击。


**功能演示**
-
- 注册与登录
![register&login.gif](https://i.loli.net/2019/07/14/5d2ac5391870560571.gif)

- 微博与评论
![weibo&comment.gif](https://i.loli.net/2019/07/14/5d2ac5387e63c59927.gif)

- 防御 `XSS` 攻击
![xss-defense.gif](https://i.loli.net/2019/07/14/5d2ac53fec1a536224.gif)


- 留言
![message.gif](https://i.loli.net/2019/07/14/5d2ac5366b54213623.gif)

- 查看所有评论过的微博
![all-comments.gif](https://i.loli.net/2019/07/14/5d2ac535df65c57772.gif)

- 管理员修改用户密码
![change-password.gif](https://i.loli.net/2019/07/14/5d2ac539c6fc628772.gif)



**依赖**



**如何运行**