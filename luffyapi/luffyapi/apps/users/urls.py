from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path, re_path
from . import views
urlpatterns = [
    path("login/", obtain_jwt_token ), # 视图类.as_view()
    path("capcha/", views.CaptchaAPIView.as_view() ),
    re_path("mobile/(?P<mobile>1[3-9]\d{9})/", views.MobileAPIView.as_view() ),
    re_path("sms/(?P<mobile>1[3-9]\d{9})/", views.SMSAPIView.as_view() ),
    path("", views.UserCreateAPIView.as_view() ),
]