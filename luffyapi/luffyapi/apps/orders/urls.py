from django.urls import path,re_path
from . import views
urlpatterns = [
    path("",views.OrderCreateAPIView.as_view()),
    path("list/",views.OrderListAPIView.as_view()),
]