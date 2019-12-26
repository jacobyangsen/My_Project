from rest_framework import serializers
from .models import Banner
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播广告序列化器"""
    class Meta:
        model = Banner
        fields = ["image","link","name"]

from .models import Nav
class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Nav
        fields = ["name","link","opt","is_http"]