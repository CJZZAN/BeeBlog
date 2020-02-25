from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django import forms
from django.forms import widgets, fields
from main import models
from django.contrib import messages

# Create your views here.
class RegisterAuth(forms.Form):
    Name = fields.CharField(max_length=12, min_length=2, error_messages={'required': '昵称不能为空',
                                                                         'max_length': '昵称长度不能大于12',
                                                                         'min_length': '昵称长度不能小于2'},
                            widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'Name',
                                                            'placeholder': 'Tony-stark'}))
    Email = fields.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
                              widget=widgets.EmailInput(attrs={'class': 'form-control', 'name': 'Email',
                                                               'placeholder': 'xxxx@163.com'}))
    Password = fields.CharField(max_length=12, min_length=6, error_messages={'required': '密码不能为空',
                                                                             'max_length': '密码长度不能大于12',
                                                                             'min_length': '密码长度不能小于6'},
                                widget=widgets.PasswordInput(attrs={'class': 'form-control', 'name': 'Password',
                                                                    'placeholder': 'Password'}))
    Birthday = fields.DateField(error_messages={'required': '生日不能为空', 'invalid': '生日格式错误'},
                                widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'Birthday',
                                                                'placeholder': '1995-09-20'}))
    PhoneNum = fields.CharField(max_length=12, min_length=8, error_messages={'required': '手机号码不能为空',
                                                                             'max_length': '手机号码长度不能大于12',
                                                                             'min_length': '手机号码长度不能小于6'},
                                widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'PhoneNum',
                                                                'placeholder': '18102588262'}))
    Hobby = fields.CharField(max_length=12, error_messages={'required': '爱好不能为空',
                                                            'max_length': '爱好长度不能大于12', },
                             widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'Hobby',
                                                             'placeholder': '写代码、装B'}))


def login(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        pwd = request.POST.get('pwd', None)
        remember = request.POST.get('remember', None)
        id = ""
        try:
            id = models.User.objects.get(user_email=email).user_id
        except:
            pass
        if email and pwd:
            try:
                user = models.User.objects.get(user_email=email)
            except:
                return HttpResponse("FAILED")
            name = user.user_name
            if user.user_password == pwd:
                request.session['useremail'] = email
                request.session['is_login'] = True
                request.session['username'] = name
                request.session['user_id'] = id
                if remember == 'true':
                    # 设置为None，则表示使用全局的过期时间
                    request.session.set_expiry(None)
                else:
                    # 设置浏览器关闭之后就过期
                    request.session.set_expiry(0)
                return HttpResponse("OK")
            return HttpResponse("FAILED1")
        return HttpResponse("FAILED2")
    return render(request, 'login.html')


def login_check(func, *args, **kwargs):
    def wrapper(request,*args,**kwargs):
        if request.session.get('is_login', None):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/login')
    return wrapper


def register(request):
    if request.method == "GET":
        obj = RegisterAuth()
        return render(request, 'register.html', {'obj': obj})
    if request.method == "POST":
        obj = RegisterAuth(request.POST)
        request_form = obj.is_valid()
        if request_form:
            name = request.POST.get('Name')
            email = request.POST.get('Email')
            birthday = request.POST.get('Birthday')
            password = request.POST.get('Password')
            sex = request.POST.get('Sex')
            phonenum = request.POST.get('PhoneNum')
            hobby = request.POST.get('Hobby')
            if not models.User.objects.filter(user_email=email):
                models.User.objects.create(user_name=name, user_email=email, user_password=password,
                                           user_birth=birthday, user_sex=sex, user_phonenum=phonenum, user_hobby=hobby)
                messages.success(request, "注册成功!")

                return redirect('/login/register')
            messages.success(request,"邮箱已被注册")
            return redirect('/login/register')
        return render(request, 'register.html', {'obj': obj})


EMAIL = ''

def findpsw(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        phonenum = request.POST.get('phonenum', None)
        birthday = request.POST.get('birthday', None)
        hobby = request.POST.get('hobby', None)
        if email and phonenum and birthday and hobby:
            try:
                user = models.User.objects.get(user_email=email)
            except:
                return HttpResponse("FAILED")
            if user.user_phonenum == phonenum and user.user_birth == birthday and user.user_hobby == hobby:
                request.session['username'] = email
                request.session['is_psw'] = True
                request.session.set_expiry(0)
                global EMAIL
                EMAIL = email
                print(EMAIL)
                return HttpResponse("OK")
            return HttpResponse("FAILED1")
        return HttpResponse("FAILED2")
    return render(request,'findpsw.html')

def setpsw_check(func, *args, **kwargs):
    def wrapper(request):
        if request.session.get('is_psw', None):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/login')
    return wrapper

@setpsw_check
def setpsw(request):
    if request.method == "POST":
        password = request.POST.get('password',None)
        passwordack = request.POST.get('passwordack',None)
        if password and passwordack:
            if password == passwordack:
                result = models.User.objects.get(user_email=EMAIL)
                oldpsw = result.user_password
                if password != oldpsw:
                    result.update(user_password = password)
                    messages.success(request, "修改密码成功!")
                    return HttpResponse("OK")
                return HttpResponse("FAILED")
            return HttpResponse("FAILED1")
        return HttpResponse("FAILED2")
    else:
        request.session['is_psw'] = False
        return render(request,'setpsw.html')
