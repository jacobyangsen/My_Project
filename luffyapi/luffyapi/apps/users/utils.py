from luffyapi.settings import constants
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token   jwt认证信息
    :param user    根据客户端提交的信息查询出来的用户模型对象
    :param request 本次客户端提交的请求对象
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        # 返回用户积分和换算比例
        'user_credit': user.credit,
        'credit_rmb': constants.RMB_CREDIT,
    }

from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q

def get_user_by_account(username):
    return User.objects.filter( Q(username=username) | Q(mobile=username) ).first()

class UsernameMobileAuthBackend(ModelBackend):
    # 重写认证类里面的认证方法，实现多条件登录
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user

