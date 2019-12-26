from django.urls import path,re_path
from . import views
urlpatterns = [
    path("alipay/",views.AlipayAPIView.as_view()),
    path('alipay/result/', views.AlipayResultAPIView.as_view()),
]