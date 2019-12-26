from django.urls import path
from . import views
urlpatterns = [
    path("", views.CartAPIViewSet.as_view({
        "post":"add_cart",
        "get":"list",
        "patch":"change_select_status",
        "delete":"delete",
        "put": "change_course_expire",
    }) ),
    path("selected/", views.CartAPIViewSet.as_view({"get":"get_selected_course"})),
]