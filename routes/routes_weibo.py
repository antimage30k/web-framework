from models.comment import Comment
# from models.user import User
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
    escape)
from utils import log


@login_required
def index(request):
    """
    weibo 首页的路由函数
    """
    if 'id' in request.query:
        user_id = int(request.query['id'])
        u = User.one(id=user_id)
    else:
        u = current_user(request)

    weibos = Weibo.all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    form.update(user_id=u.id)
    # 转义以防御 xss 攻击
    form = escape(form)
    Weibo.new(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


# @weibo_owner_required
# def delete(request):
#     weibo_id = int(request.query['id'])
#     Weibo.delete(weibo_id)
#     # 注意删除所有微博对应评论
#     # 使用all方法替换find_all
#     cs = Comment.all(weibo_id=weibo_id)
#     for c in cs:
#         c.delete(c.id)
#     return redirect('/weibo/index')


def weibo_owner_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        # 使用one方法从数据库中查询
        w = Weibo.one(id=int(weibo_id))
        log('weibo owner', weibo_id, u.id, w)
        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


@login_required
@weibo_owner_required
def edit(request):
    weibo_id = int(request.query['id'])
    # 使用one方法替换find_by
    w = Weibo.one(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


@login_required
@weibo_owner_required
def update(request):
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form()
    # u = current_user(request)
    weibo_id = int(form['id'])
    content = form['content']
    Weibo.update(weibo_id, content=content)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


@login_required
@weibo_owner_required
def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    # 注意删除所有微博对应评论
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)
    return redirect('/weibo/index')


@login_required
def comment_add(request):
    u = current_user(request)
    form = request.form()
    weibo_id = int(form['weibo_id'])
    # 转义以防御 xss 攻击
    form = escape(form)
    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo_id
    # 以c的attributes的字典为参数
    Comment.new(c.__dict__)
    w = Weibo.one(id=c.weibo_id)
    weibo_owner = User.one(id=w.user_id)

    log('comment add', c, u, form)
    return redirect('/weibo/index?id={}'.format(weibo_owner.id))


def comment_owner_required(route_function):
    # 根据是否是评论作者分发路由
    def func(request):
        u = current_user(request)
        if 'comment_id' in request.query:
            comment_id = request.query['comment_id']
        else:
            comment_id = request.form()['comment_id']
        c = Comment.one(id=int(comment_id))
        if c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')
    return func


def comment_owner_or_weibo_owner_required(route_function):
    # 根据是否是评论作者或微博作者来决定权限
    def func(request):
        u = current_user(request)
        if 'comment_id' in request.query:
            comment_id = request.query['comment_id']
        else:
            comment_id = request.form()['comment_id']
        c = Comment.one(id=int(comment_id))
        if c.user_id == u.id:
            return route_function(request)
        else:
            # 不是评论作者，进一步判断是否是微博作者
            w = Weibo.one(id=c.weibo_id)
            if w.user_id == u.id:
                return route_function(request)
            else:
                return redirect('/weibo/index')
    return func


# 只有该评论所属微博作者和评论作者能删除评论
@login_required
@comment_owner_or_weibo_owner_required
def comment_delete(request):
    comment_id = int(request.query['comment_id'])
    Comment.delete(comment_id)
    # 删除之后重定向
    return redirect('/weibo/index')


# 只有该评论作者能修改评论
@login_required
@comment_owner_required
def comment_edit(request):
    comment_id = int(request.query['comment_id'])
    c = Comment.one(id=comment_id)
    # 返回一个修改评论的页面
    return html_response('comment_edit.html', comment=c)


# 只有该评论作者能修改评论
@login_required
@comment_owner_required
def comment_update(request):
    form = request.form()
    # 根据form更新评论，再重定向回weibo/index
    # u = current_user(request)
    comment_id = int(form['comment_id'])
    # c = Comment.one(id=comment_id)
    # weibo_id = c.weibo_id
    content = form['content']
    Comment.update(comment_id, content=content)
    return redirect('/weibo/index')


@login_required
def commented(request):
    u = current_user(request)
    ws = (
        Weibo.select(Weibo.connection)
             .join(Comment, 'id', 'weibo_id')
             .where('comment', 'user_id', u.id)
             .all()
    )
    # group_by('weibo', 'id')
    log('commented weibos', ws)
    ws = handle_commented(ws)
    return html_response('weibo_commented.html', weibos=ws, user=u)


def handle_commented(ws):
    '''
    {
    'id': 1,
    'user_id': 1,
    'content':
    'WELCOME! My 10th Birthday!',
    'comment.id': 1,
    'weibo_id': 1,
    'comment.user_id': 1,
    'comment.content': 'Happy Birthday!'
    }
    '''
    for w in ws:
        w['comment_username'] = User.one(id=w['comment.user_id']).username
        w['comment_content'] = w['comment.content']
        w['username'] = User.one(id=w['user_id']).username
        w['comment_id'] = w['comment.id']
        w['comment_user_id'] = w['comment.user_id']
    log('handled commented', ws)
    return ws


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': delete,
        # '/weibo/delete': delete,
        '/weibo/edit': edit,
        '/weibo/update': update,
        '/weibo/index': index,
        '/weibo/commented': commented,
        # 评论功能
        '/comment/add': comment_add,
        '/comment/edit': comment_edit,
        '/comment/update': comment_update,
        '/comment/delete': comment_delete,
    }
    return d
