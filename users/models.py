from django.db import models
# 导入django内置的一个用户User模型，然后通过一对一关联关系为默认的User扩展用户数据
from django.contrib.auth.models import User

# Create your models here.

'''
点击User进入django内部去看User模型的源码，可以看到他是继承了`AbstractUser`类的所有数据，我们再去看一下`AbstractUser`都有哪些数据？可以看到它里边创建了用户的几个基本信息,用户名称`username`、`first_name`、`last_name`、`email`、`is_staff`、`is_active`、`date_joined`，这几个字段远远不能全面记录一个用户的信息，比如我们还想知道用户的性别、手机号、个人介绍、让用户还拥有自己的头像，那么我们就得去扩展用户的模型。

扩展用户模型的方法有两种，一种是模仿官方的方法，直接继承`AbstractUser`类来扩展用户数据，另外一种是通过一对一关系关联User类，来扩展用户数据，我这里选择采用第二种一对一关联的方式来扩展，这样的好处是不需要再setiings.py中另外配置，也有利于我们理解和学习django的关联关系用法。
'''


class UserProfile(models.Model):
    '''
    定义用户类
    通过一对一关联django内置的User类进行扩展
    '''
    USER_GENDER_TYPE = (
        ('男', '男'),
        ('女', '女')
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nike_name = models.CharField('昵称', max_length=50, blank=True, default='')
    birthday = models.DateTimeField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=6, default='男', choices=USER_GENDER_TYPE)
    address = models.CharField('地址', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name='用户头像')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


class EmailVerifyRecord(models.Model):
    '''
    邮箱验证码字段
    '''
    SEND_TYPE_CHOICES = {
        ('register', '注册'),
        ('forger', '找回密码')
    }
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
