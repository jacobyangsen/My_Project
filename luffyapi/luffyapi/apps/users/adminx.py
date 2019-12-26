import xadmin

from .models import Credit
class CreditModelAdmin(object):
    """用户积分收支记录"""
    list_display=["user","create_time","operation","number"]
xadmin.site.register(Credit, CreditModelAdmin)