"""
custom_reg_form Django application initialization.
"""

from django.apps import AppConfig


class CustomRegFormConfig(AppConfig):
    """
    Configuration for the custom_reg_form Django application.
    """

    name = 'custom_reg_form'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'custom_reg_form',
                'regex': r'^api/custom-reg-form/v1/',
                'relative_path': 'urls',
            },
        },
    }
