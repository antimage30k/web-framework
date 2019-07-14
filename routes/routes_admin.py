from models.user import User, UserRole
from models.weibo import Weibo
from routes import redirect, current_user, html_response

from utils import log


# 判断admin权限
def admin_required(route_function):
    def func(request):
        u = current_user(request)
        log('role', u.role, UserRole.admin.name)
        if u.role == UserRole.admin.name:
            return route_function(request)
        else:
            return redirect('/user/login/view')
    return func


# admin用户管理主页
@admin_required
def route_admin_users(request):
    users = User.all()
    return html_response('admin_users.html', users=users)


# 修改用户密码的路由函数
@admin_required
def admin_edit_password(request):
    # 从url的query部分拿到用户id
    user_id = int(request.query['id'])
    u = User.one(id=user_id)
    # 返回编辑页面
    return html_response('admin_password_edit.html', user=u)


# 更新密码的函数
@admin_required
def update_user_password(request):
    # 拿到表单
    form = request.form()
    # 更新数据
    User.update_password(form)
    # 重定向回主页
    return redirect('/admin/users')


def route_admin_weibo_all(request):
    u = current_user(request)
    weibos = Weibo.all()
    # 替换模板文件中的标记字符串
    return html_response('weibo_index.html', weibos=weibos, user=u)


# 路由字典
def route_dict():
    d = {
        '/admin/users': route_admin_users,
        '/admin/edit/password': admin_edit_password,
        '/update/user/password': update_user_password,
        '/admin/weibo/all': route_admin_weibo_all,
    }
    return d
