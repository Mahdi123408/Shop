from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from products.models import Product
from utils.auth import check_auth

class HomeView(View):
    def get(self, request: HttpRequest):
        user = check_auth(request)
        data = {}
        data['product_home'] = Product.objects.filter(is_home_index=True, is_active=True, deleted=False).first()
        data['products'] = Product.objects.filter(is_active=True, deleted=False)[:10]
        if user[0]:
            mes = None
            if 'mes' in request.session:
                mes = request.session.get('mes')
                del request.session['mes']
            data['mes'] = mes
            data['custom_user'] = user[1]
        return render(request, 'home/index.html', data)
