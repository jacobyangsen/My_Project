"""luffyapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.views.static import serve
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path(r'xadmin/', xadmin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('home/', include("home.urls")),
    path('user/', include("users.urls")),
    path('courses/', include("courses.urls") ),
    path('cart/', include("cart.urls") ),
    path('orders/', include("orders.urls") ),
    path('coupon/', include("coupon.urls")),
    path('payments/', include('payments.urls')),
]
