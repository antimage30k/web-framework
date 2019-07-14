from models.todo import Todo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    todos = Todo.all(user_id=u.id)
    # 替换模板文件中的标记字符串
    return html_response('todo_index.html', todos=todos)


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    form.update(user_id=u.id)
    Todo.new(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo/index')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.one(id=todo_id)
    return html_response('todo_edit.html', todo=t)


def update(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    todo_id = form['id']
    title = form['title']
    Todo.update(todo_id, title=title)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo/index')


def same_user_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.one(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index')

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo/add': login_required(add),
        '/todo/delete': login_required(same_user_required(delete)),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
        '/todo/index': login_required(index),
    }
    return d
