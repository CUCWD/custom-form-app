"""URLs for custom_reg_form."""

from django.urls import re_path

from .views import account, me


urlpatterns = [
    re_path(r'^api/custom-reg-form/v1/me/$', me, name='custom_reg_form_me'),
    re_path(
        r'^api/custom-reg-form/v1/accounts/(?P<username>[-\w.@+]+)/$',
        account,
        name='custom_reg_form_account',
    ),
]
