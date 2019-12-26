from django.db import models
from luffyapi.utils.models import BaseModel

# Create your models here.
class Banner(BaseModel):
    """轮播广告"""
    image = models.ImageField(upload_to="banner",blank=True, null=True, verbose_name="广告图片")
    name = models.CharField(max_length=255,blank=True, null=True, verbose_name="广告标题")
    link = models.CharField(max_length=512,blank=True, null=True, verbose_name="广告链接")
    note = models.TextField(verbose_name='备注信息')

    class Meta:
        db_table = 'ly_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Nav(BaseModel):
    """
    导航
    """
    NAV_POSITION = (
        (0, '头部导航'),
        (1, '底部导航'),
    )
    name = models.CharField(max_length=50, verbose_name='导航名称')
    link = models.CharField(max_length=250, verbose_name='导航地址')
    opt = models.SmallIntegerField(choices=NAV_POSITION, default=0, verbose_name='显示位置')
    is_http = models.BooleanField(default=False, verbose_name="是否站外导航")

    class Meta:
        db_table = 'ly_nav'
        verbose_name = '导航'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name