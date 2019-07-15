from models.message import Message
from models.user import User
from routes import escape, redirect, html_response, current_user, json_response
from utils import log


def index(request):
    u = current_user(request)
    # ms = Message.all()
    return html_response('messages.html', username=u.username)


def show(request):
    ms = (
        Message.select(Message.connection)
               .join(User, 'user_id', 'id')
               .all()
    )
    return json_response(ms)


def add(request):
    u = current_user(request)
    form = request.json()
    form['user_id'] = u.id
    form = escape(form)
    log('ajax message add', form, u)
    m = Message.new(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    message = dict(message='成功添加 {}'.format(m.content))
    return json_response(message)
    # form = request.form()
    # # 转义以防御 xss 攻击
    # form = escape(form)
    # Message.new(form)
    # # 浏览器发送数据过来被处理后, 重定向到首页
    # # 浏览器在请求新首页的时候, 就能看到新增的数据了
    # return redirect('/message/index')


def route_dict():
    d = {
        '/message/index': index,
        '/message/add': add,
        '/message/show': show,
    }
    return d
