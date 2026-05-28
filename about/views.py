from django.shortcuts import render
from django.views import View

from utils.auth import check_auth


class AboutView(View):
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
            return render(request, 'about/about.html', data)
        else:
            return render(request, 'about/about.html', {'mes': mes})
