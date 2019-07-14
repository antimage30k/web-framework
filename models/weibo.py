from models.base_model import SQLModel
from models.comment import Comment


class Weibo(SQLModel):
    """
    微博类
    """
    # 创建weibo表的sql语句，以user_id作为索引
    sql_create = '''
    CREATE TABLE `weibo` (
        `id`            INT NOT NULL AUTO_INCREMENT,
        `user_id`       INT NOT NULL,
        `content`       VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `user_id_index` (`user_id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    # @classmethod
    # def add(cls, form, user_id):
    #     w = Weibo(form)
    #     w.user_id = user_id
    #     weibo_form = form.update(user_id=user_id)
    #     w.new(weibo_form)
    #
    # @classmethod
    # def update(cls, form):
    #     weibo_id = int(form['id'])
    #     w = Weibo.one(id=weibo_id)
    #     w.content = form['content']
    #     w.update(weibo_id)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs
