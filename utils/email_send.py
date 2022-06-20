from django.core.mail import send_mail
import random, string

from users.models import EmailVerifyRecord


# 生成长度为8的随机验证码
def random_str():
    chars = string.digits + string.ascii_letters
    str_code = random.sample(chars, 8)
    return "".join(str_code)


# 保存验证码，并发送带有验证码的链接
def send_register_email(email, send_type='register'):
    # 保存验证码
    email_recode = EmailVerifyRecord()
    code = random_str()
    email_recode.code = code
    email_recode.email = email
    email_recode.send_type = send_type
    email_recode.save()
    # 保存验证码之后，把带有验证码的链接发送到注册的邮箱
    if send_type == 'register':
        email_title = '账号注册激活链接'
        email_body = '请点击此链接以激活您的账号：http://127.0.0.1:8000/users/active/{}'.format(code)
        send_status = send_mail(email_title, email_body, 'guishoushi126@126.com', [email])
        if send_status:
            pass
