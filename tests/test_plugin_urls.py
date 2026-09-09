import custom_reg_form
from django.test import SimpleTestCase
from django.urls import include, re_path, resolve

from custom_reg_form.apps import CustomRegFormConfig
from custom_reg_form.views import account, me


mounted_urlpatterns = (
    re_path(
        r'^api/custom-reg-form/v1/',
        include(('custom_reg_form.urls', 'custom_reg_form'), namespace='custom_reg_form'),
    ),
)


class PluginUrlsTests(SimpleTestCase):
    """Tests for the LMS plugin registration and mounted route resolution."""

    def test_lms_plugin_registration(self):
        plugin_config = CustomRegFormConfig('custom_reg_form', custom_reg_form)

        self.assertIsNotNone(plugin_config.plugin_app)
        self.assertIn('url_config', plugin_config.plugin_app)
        self.assertIn('lms.djangoapp', plugin_config.plugin_app['url_config'])

        url_config = plugin_config.plugin_app['url_config']['lms.djangoapp']
        self.assertEqual(url_config['namespace'], 'custom_reg_form')
        self.assertEqual(url_config['regex'], r'^api/custom-reg-form/v1/')
        self.assertEqual(url_config['relative_path'], 'urls')

    def test_me_route_resolves_through_mounted_prefix(self):
        match = resolve('/api/custom-reg-form/v1/me/', urlconf=mounted_urlpatterns)

        self.assertEqual(match.func, me)
        self.assertEqual(match.url_name, 'custom_reg_form_me')

    def test_account_route_resolves_through_mounted_prefix(self):
        match = resolve('/api/custom-reg-form/v1/accounts/alice/', urlconf=mounted_urlpatterns)

        self.assertEqual(match.func, account)
        self.assertEqual(match.kwargs['username'], 'alice')
