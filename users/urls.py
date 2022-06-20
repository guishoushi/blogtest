"""
@Author : guishoushi
@File : urls.py
@Project : blogtest
@Time : 2022/6/15 17:46
"""

from django.urls import path
from users import views

# 定义一个命名空间，用来区分不同应用之间的链接地址
app_name = 'urls'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('active/<active_code>', views.ActiveUser.as_view(), name='active')
]
