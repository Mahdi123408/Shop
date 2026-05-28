from django.shortcuts import render
from django.views import View
from django.http import HttpRequest

from utils.auth import check_auth


class ContactUsView(View):
    def get(self, request):
        mes = None
        if 'mes' in request.session:
            mes = request.session.get('mes')
            del request.session['mes']
        user = check_auth(request)
        if user[0]:
            data = {
                'custom_user': user[1],
                'mes': mes
            }
            return render(request, 'contact_us/contact_us.html', data)
        else:
            return render(request, 'contact_us/contact_us.html', {'mes': mes})

