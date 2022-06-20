"""
@Author : guishoushi
@File : forms.py
@Project : blogtest
@Time : 2022/6/16 17:51
"""
from django.forms import *
from users.models import UserProfile, User


class LoginForm(Form):
    '''
    LoginFrom
    登录表单
    '''
    username = CharField(label='用户名', max_length=30,
                         error_messages={'max_length': '用户名不能长度不能超过10位'},
                         widget=TextInput(
                             attrs={'class': 'form-control',
                                    'placeholder': '请输入用户名：'}
                         ))
    password = CharField(label='用户密码',
                         min_length=6,
                         error_messages={'min_length': '密码长度不能少于6位'},
                         widget=PasswordInput(
                             attrs={'class': 'form-control',
                                    'placeholder': '请输入密码：'}
                         ))

    # 局部钩子方法  重写password字段的钩子方法
    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        # 判断用户名和密码一样
        if password == username:
            # 抛出对应的错误
            raise ValidationError('账号和密码不能一致！')
        # return 这个对应绑定的字段
        return password


class RegisterForm(ModelForm):
    '''
    用户注册时的表单
    '''
    email = EmailField(label='用户邮箱',
                       min_length=3,
                       widget=EmailInput(
                           attrs={'class': 'form-control',
                                  'placeholder': '请输入邮箱：'}))

    # error_messages={} 自定义错误信息 建议用默认信息就行
    password1 = CharField(label='确认密码',
                          min_length=6,
                          error_messages={'min_length': '密码长度不能少于6位'},
                          widget=PasswordInput(
                              attrs={'class': 'form-control',
                                     'placeholder': '请输入确认密码：'}
                          ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': TextInput(
                attrs={'class': 'form-control',
                       'placeholder': '请输入用户名：'}),

            'password': PasswordInput(
                attrs={'class': 'form-control',
                       'placeholder': '请输入密码：'})
        }

    # 重写password1字段的钩子方法
    # 自定义 局部的钩子方法 判断两次密码输入是否一致
    def clean_password1(self):
        # 获取通过验证的密码，判断两次输入的密码是否一致
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        # 如果两次输入的密码不一致，抛出对应的错误
        if password != password1:
            raise ValidationError('两次密码输入不一致，请重新确认！')
        # return 对应的字段
        return password1

    # 定义局部钩子方法，判断email是否已经存在
    def clean_email(self):
        # 获取通过验证的email
        email = self.cleaned_data.get('email')
        exists_email = User.objects.filter(email=email).first()
        if exists_email:
            raise ValidationError('已存在一位使用该邮箱的用户。')
        return email
