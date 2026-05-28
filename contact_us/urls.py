from django.urls import path
from contact_us.views import ContactUsView

urlpatterns = [
        path('', ContactUsView.as_view() , name='contact_us'),
]