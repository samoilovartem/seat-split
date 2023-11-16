from django.urls import path

from apps.support.api.v1.contact_us import ContactView

urlpatterns = [
    path('contact-us/', ContactView.as_view(), name='contact-us'),
]
