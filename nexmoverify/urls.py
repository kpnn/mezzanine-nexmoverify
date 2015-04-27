from django.conf.urls import patterns, url

from nexmoverify.views import  secret, add_phone, password_reset

urlpatterns = patterns('',

    url(r'accounts/phone/add$',add_phone, name='add_phone'),
    url(r'accounts/phone/passwordreset$',password_reset, name='password_reset_phone'),
    url(r'test/secret$', secret)
                       
)
