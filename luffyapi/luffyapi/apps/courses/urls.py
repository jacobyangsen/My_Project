from django.urls import path,re_path
from . import views
urlpatterns = [
    path("category/",views.CourseCategoryListAPIView.as_view()),
    path("",views.CourseListAPIView.as_view()),
    re_path("(?P<pk>\d+)/", views.CourseRetrieveAPIView.as_view()),
    path("chapters/", views.CourseChapterListAPIView.as_view()),
    path("player/", views.PolyvAPIView.as_view()),
]