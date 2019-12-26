from rest_framework.generics import ListAPIView
from .models import CourseCategory
from .serializers import CourseCategoryModelSerializer
class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders","-id")
    serializer_class = CourseCategoryModelSerializer
    # 设置不分页，提前写这段代码的作用就是防止将来如果进行全局分页，可以不被它干扰到
    pagination_class = None

from .models import Course
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CoursePageNumberPagination
class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders", "-id")
    serializer_class = CourseModelSerializer
    pagination_class = CoursePageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['course_category']
    ordering_fields = ['id', 'students', 'price']

from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveModelSerializer
class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True)
    serializer_class = CourseRetrieveModelSerializer

from rest_framework.generics import ListAPIView
from .models import CourseChapter
from .serializers import CourseChapterModelSerializer
class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("chapter")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course', ]


"""课时视频播放接口"""
from luffyapi.libs.polyv import PolyvPlayer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.response import Response
class PolyvAPIView(APIView):
    """保利威云视频服务token api接口"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取视频播放的token"""
        userId = settings.POLYV_CONFIG["userId"]
        secretkey = settings.POLYV_CONFIG["secretkey"]
        tokenUrl = settings.POLYV_CONFIG["tokenUrl"]
        polyv = PolyvPlayer(userId,secretkey,tokenUrl)
        vid = request.query_params.get("vid")
        user_ip = request.META.get("REMOTE_ADDR")  # 用户的IP
        user_id = request.user.id      # 用户ID
        user_name = request.user.username  # 用户名

        result = polyv.get_video_token(vid, user_ip, user_id, user_name)
        return Response(result.get("token"))