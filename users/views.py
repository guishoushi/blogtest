from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
# 导入Django中自带的用户认证方法
from django.contrib.auth import authenticate, login, logout, backends
from django.views import View
from django.db.models import Q

from users.forms import LoginForm, RegisterForm, User
from users.models import EmailVerifyRecord
from utils.email_send import send_register_email


# Create your views here.

class MyBackend(backends.ModelBackend):
    '''
    主要实现既可以用户名登录也可以使用邮箱登录的功能
    要记得在settings中配置以下字段才会生效
    AUTHENTICATION_BACKENDS = (
    # 这是使用自己写的
    'users.views.MyBackend',
    # 这是django默认使用的认证
    # 'django.contrib.auth.backends.ModelBackend',)
    '''

    # 重写该方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Q 的作用是 可以通过& 和 | 连接起来 当操作符在两个Q对象之间时 会生成一个新的Q对象
            # Q的详细用法可查看该地址  https://www.toutiao.com/article/6809613183938986500/
            # 该表达式的意思是 如果username=username 或者 email=username
            # 实现的具体效果是 无论用户使用用户名登录还是邮箱登录都可以
            user = User.objects.get(Q(username=username) | Q(email=username))
            # 通过check_password() 将用户的明文密码加密成哈希值
            # self.user_can_authenticate(user) 判断用户是否为可用状态，如果被禁用状态，无法通过认证,建议加上
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            return


class Login(View):
    '''
    用户登录的视图
    '''

    def get(self, request):
        form = LoginForm()
        data = {
            'form': form
        }
        return render(request, template_name='users/login.html', context=data)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 获取前端表单提交的用户名，密码
            username = request.POST.get('username')
            password = request.POST['password']
            # 与数据库中的用户名和密码进行比较，django默认保存密码是哈希形式，并不是明文，这里的password验证调用的是User类中的check_password方法，以哈希值比较
            user = authenticate(request, username=username, password=password)
            # 如果验证用户验证成功，
            if user:
                # 登录成功
                login(request, user)
                return HttpResponse('登录成功！')
            # 从数据库查询出用户，判断账号是否激活
            user = User.objects.filter(username=username).first()
            # 如果账号存在，并且属于未激活状态
            if user and not user.is_active:
                return HttpResponse(f'账号需激活后才可使用，请移步至您的邮箱({user.email})激活该账号。')
        return render(request, template_name='users/login.html', context={'form': form, 'error': '账号或密码错误!'})


class Register(View):
    '''
    users模块：用户注册的处理视图
    '''

    def get(self, request):
        form = RegisterForm()
        return render(request, template_name='users/register.html', context={'form': form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            # commit=False 是将通过验证的数据生成一个数据对象，暂时保存到内存中，不直接写入数据库，
            # 等待用set_password()方法将密码转换为哈希值后，再去保存，
            # 否则django只保存用户名不会保存密码，但可以在后台中手动修改密码
            new_user = form.save(commit=False)
            # set_password() 是将明文的密码加密成哈希值之后，再去保存，否则django只保存用户名，不保存密码
            new_user.set_password(form.cleaned_data.get('password'))
            # 将用户的有效性设置为False，is_active需要为True账号才能使用
            new_user.is_active = False
            # 等带用户密码通过set_password()加密之后再将数据写入数据库
            new_user.save()
            # 调用发送激活账号的邮件给用户
            email = form.cleaned_data.get('email')
            send_register_email(email, 'register')
            # 用户注册成功，提醒用户去邮箱中接收邮件激活账号
            return HttpResponse('账号注册成功，激活邮件已成功发送至您的邮箱，账号需激活后才可使用，请移步至您的邮箱。')
        return render(request, template_name='users/register.html', context={'form': form})


class ActiveUser(View):
    '''
    用户通过邮箱激活账号的视图
    如果能根据验证码查询到用户，那么就激活这个用户，允许登录到后台
    '''

    def get(self, request, active_code):
        print('用户提交的验证码：', active_code)
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        print('查询到的数据：', all_records)
        if all_records:
            for record in all_records:
                email = record.email
                print(email)
                user = User.objects.filter(email=email).first()
                print(user)
                user.is_active = True
                user.save()
        else:
            return HttpResponse('链接有误！')
        return redirect('urls:login')
