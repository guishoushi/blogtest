from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import *
# 首先引入User
from django.contrib.auth.models import User

# 必须通过unregister将User注销
admin.site.unregister(User)


# Register your models here.

# 定义关联的对象样式 ，Stackedlnline为纵向排列
class UserProfilelnlines(admin.StackedInline):
    model = UserProfile


# 关联字段在User之内编辑
class AdminUserProfile(UserAdmin):
    inlines = [UserProfilelnlines]


# 邮箱验证码字段
class AdminEmailVerifyRecord(admin.ModelAdmin):
    list_display = ('code', 'email', 'send_type', 'send_time')


# 重新注册User
admin.site.register(User, AdminUserProfile)
# 注册邮箱验证码模型
admin.site.register(EmailVerifyRecord, AdminEmailVerifyRecord)
