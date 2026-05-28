from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from utils.auth import check_auth, login
from .models import CustomUser


class LoginView(View):
    def get(self, request: HttpRequest):
        user = check_auth(request)
        if user[0]:
            return redirect('home')
        else:
            mes = None
            if 'mes' in request.session:
                mes = request.session.get('mes')
                del request.session['mes']
            return render(request, 'auth/login/login.html', {'mes': mes})

    def post(self, request):
        user = check_auth(request)
        if user[0]:
            return redirect('home')
        else:
            if 'username' in request.POST and 'password' in request.POST:
                check_login = login(request, request.POST['username'], request.POST['password'])
                if check_login[0]:
                    return redirect('home')
                else:
                    request.session['mes'] = 'نام کاربری یا رمز  عبور اشتباه است .'
                    return redirect('login')


class RegisterView(View):
    def get(self, request: HttpRequest):
        user = check_auth(request)
        if user[0]:
            return redirect('home')
        else:
            mes = None
            if 'mes' in request.session:
                mes = request.session.get('mes')
                del request.session['mes']
            return render(request, 'auth/register/register.html', {'mes': mes})

    def post(self, request: HttpRequest):
        user = check_auth(request)
        if user[0]:
            return redirect('home')
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if (
                    not first_name or
                    not last_name or
                    not username or
                    not phone_number or
                    not email or
                    not password or
                    not confirm_password
            ):
                request.session['mes'] = 'لطفاً تمام فیلدها را پر کنید.'
                return redirect('register')
            if password != confirm_password:
                request.session['mes'] = 'رمز عبور و تکرار آن یکسان نیست.'
                return redirect('register')
            if CustomUser.objects.filter(username=username).exists():
                request.session['mes'] = 'این نام کاربری قبلاً ثبت شده است.'
                return redirect('register')
            if CustomUser.objects.filter(email=email).exists():
                request.session['mes'] = 'این ایمیل قبلاً ثبت شده است.'
                return redirect('register')

            # بررسی شماره تلفن
            if len(phone_number) != 11 or not phone_number.isdigit():
                request.session['mes'] = 'شماره تلفن معتبر نیست.'
                return redirect('register')
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone_number=phone_number,
                email=email,
                password=''  # موقت
            )
            user.set_password(password)
            # login(request, username, password)
            return redirect('home')
        except Exception as e:
            print(e)
            request.session['mes'] = 'خطایی رخ داده است.'
            return redirect('register')


class LogoutView(View):
    def get(self, request: HttpRequest):
        user = check_auth(request)
        if user[0]:
            del request.session['username']
            del request.session['password']
            request.session['mes'] = 'خروج با موفقیت انجام شد.'
            return redirect('home')
        else:
            return redirect('home')
