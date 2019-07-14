# from models import Model
# 导入SQLModel类
from models.base_model import SQLModel
from models.user import User
# from models.weibo import Weibo


class Comment(SQLModel):
    """
    评论类
    """
    # 创建comment数据库用的sql语句
    # 用weibo_id做索引
    sql_create = '''
    CREATE TABLE `comment` (
        `id`            INT NOT NULL AUTO_INCREMENT,
        `weibo_id`      INT NOT NULL,
        `user_id`       INT NOT NULL,
        `content`       VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `weibo_id_index` (`weibo_id`)
    );
    '''

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        # 修改成使用one方法
        u = User.one(id=self.user_id)
        return u

    # def weibo(self):
    #     w = Weibo.find_by(id=self.weibo_id)
    #     return w

