from django.http import HttpRequest
from accounts.models import CustomUser


def check_auth(request: HttpRequest):
    if 'username' in request.session and 'password' in request.session:
        username = request.session['username']
        password = request.session['password']
        user = CustomUser.objects.filter(username=username, is_active=True).first()
        if user and user.check_password(password):
            return True, user
        else:
            del request.session['username']
            del request.session['password']
            request.session['mes'] = 'خروج با موفقیت انجام شد وارد شوید'
            return False, 'username or password incorrect'
    else:
        return False, 'not logged in'


def login(request: HttpRequest, username: str, password: str):
    user = CustomUser.objects.filter(username=username, is_active=True).first()
    if user and user.check_password(password):
        request.session['username'] = username
        request.session['password'] = password
        return True, user
    else:
        return False, 'username or password incorrect'
