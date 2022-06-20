"""blogtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blogtest import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('users.urls'))
              ] + static(settings.STATIC_URL, documnet_root=settings.STATIC_ROOT)  # 配置静态文件url
# 配置用户上传文件url
urlpatterns += static(settings.MEDIA_URL, documnet_root=settings.MEDIA_ROOT)
