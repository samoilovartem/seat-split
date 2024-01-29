from apps.support.api.v1.contact_us import ContactView
from django.urls import path

urlpatterns = [
    path('contact-us/', ContactView.as_view(), name='contact-us'),
]
