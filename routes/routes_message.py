from models.message import Message
from routes import escape, redirect, html_response, current_user


def index(request):
    u = current_user(request)
    ms = Message.all()
    return html_response('messages.html', messages=ms, user_id=u.id)


def add(request):
    form = request.form()
    # 转义以防御 xss 攻击
    form = escape(form)
    Message.new(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/message/index')


def route_dict():
    d = {
        '/message/index': index,
        '/message/add': add,
    }
    return d
