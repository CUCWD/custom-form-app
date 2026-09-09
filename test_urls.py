"""Test URL configuration matching the LMS plugin mount."""

from django.urls import include, re_path


urlpatterns = [
    re_path(
        r'^api/custom-reg-form/v1/',
        include(('custom_reg_form.urls', 'custom_reg_form'), namespace='custom_reg_form'),
    ),
]