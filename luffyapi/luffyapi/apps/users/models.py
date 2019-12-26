from django.db import models
from django.contrib.auth.models import AbstractUser
from luffyapi.settings import constants
from luffyapi.utils.models import BaseModel
# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name="手机号码", help_text="手机号码")
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True, verbose_name="头像")
    wechat = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="微信号", help_text="微信号")
    credit = models.IntegerField(default=0, null=True, blank=True, verbose_name="用户积分",
                                 help_text="用户积分换算比例： 1RMB=%s积分" % constants.RMB_CREDIT)
    class Meta:
        db_table = 'ly_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Credit(BaseModel):
    """积分流水模型"""
    opera_choices = (
        (0, "业务充值"),
        (1, "购物消费"),
        (2, "系统赠送"),
    )
    operation = models.SmallIntegerField(choices=opera_choices, default=1,verbose_name="积分操作类型")
    number = models.IntegerField(default=0, verbose_name="积分数量")
    user   = models.ForeignKey(User, related_name='user_credits', on_delete=models.CASCADE,verbose_name="用户")

    class Meta:
        db_table = 'ly_credit'
        verbose_name = '积分'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.id

from courses.models import Course
class UserCourse(BaseModel):
    """用户的课程购买记录"""
    pay_choices = (
        (1, '用户购买'),
        (2, '免费活动'),
        (3, '活动赠品'),
        (4, '系统赠送'),
    )
    user = models.ForeignKey(User, related_name='user_courses', on_delete=models.DO_NOTHING, verbose_name="用户")
    course = models.ForeignKey(Course, related_name='course_users', on_delete=models.DO_NOTHING, verbose_name="课程")
    trade_no = models.CharField(max_length=128, null=True, blank=True, verbose_name="支付平台的流水号",
                                help_text="将来依靠流水号到支付平台查账单")
    buy_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="购买方式")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="购买时间")
    out_time = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")

    class Meta:
        db_table = 'ly_user_course'
        verbose_name = '课程购买记录'
        verbose_name_plural = verbose_name