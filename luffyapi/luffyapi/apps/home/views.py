
# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerModelSerializer
from luffyapi.settings import constants
class BannerListAPIView(ListAPIView):
    """轮播图"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders","-id")[:constants.HOME_BANNER_LENGTH]
    serializer_class = BannerModelSerializer

from .models import Nav
from .serializers import NavModelSerializer
class NavHeaderListAPIView(ListAPIView):
    """头部导航"""
    queryset = Nav.objects.filter(is_show=True, is_delete=False, opt=0).order_by("-orders","-id")[:constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer

from .serializers import NavModelSerializer
class NavFooterListAPIView(ListAPIView):
    """脚部导航"""
    queryset = Nav.objects.filter(is_show=True, is_delete=False, opt=1).order_by("-orders","-id")[:constants.FOOTER_NAV_LENGTH]
    serializer_class = NavModelSerializer
