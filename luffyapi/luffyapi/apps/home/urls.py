from django.urls import path,re_path
from . import views
urlpatterns = [
    path("banner/",views.BannerListAPIView.as_view()),
    path("nav/header/",views.NavHeaderListAPIView.as_view()),
    path("nav/footer/",views.NavFooterListAPIView.as_view()),
]