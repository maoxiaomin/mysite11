from django.shortcuts import render, redirect
from django.conf import settings
from . import models, forms
import hashlib, datetime

# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写！"
        print()
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if  not user.has_confirmed:
                    message = '该用户还未进行邮箱确认！'
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/login/index/')
                else:
                    message = '密码输入错误，请重新输入！'
            except:
                message = '用户名不正确，请重新输入！'
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '所有字段都必须填写！'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex =register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次密码输入不同'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已存在，请重新选择用户名'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经注册，请使用其他邮箱'
                    return render(request, 'login/register.html', locals())

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password =hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                return redirect('/login/login/')
        return render(request, 'login/register.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        redirect('/login/index/')
    request.session.flush()
    return redirect('/login/index/')

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的注册码！'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '邮件已经过期，原用户已失效，请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认, 请使用该账户登录！'
        return render(request, 'login/confirm.html', locals())


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = 'mtee-blog 注册确认邮件'
    text_content = '''感谢注册mtee-blog\
    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''<p><a href='http://{}/login/confirm/?code={}' target=blank>感谢注册mtee-blog</a></p>
    <p>请点击链接完成注册确认！</p>
    <p>此链接有效期为{}天！</p>'''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()