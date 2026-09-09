import json

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from custom_reg_form.models import ExtraInfo


class SelfServiceApiTests(TestCase):
    """Tests for the authenticated custom account field API."""

    FIELD_NAMES = (
        'ethnicity',
        'employment_status',
        'enrolled_in_school',
        'enrolled_in_school_type',
        'local_community_living',
        'zipcode',
    )

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='alice', password='secret')

    def test_me_requires_authentication(self):
        response = self.client.get('/api/custom-reg-form/v1/me/')

        self.assertEqual(response.status_code, 401)

    def test_me_get_creates_missing_record_and_returns_values(self):
        self.client.force_login(self.user)

        response = self.client.get('/api/custom-reg-form/v1/me/')

        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.content)
        self.assertTrue(ExtraInfo.objects.filter(user=self.user).exists())
        for field in self.FIELD_NAMES:
            self.assertIn(field, payload)
            self.assertIsNone(payload[field])

    def test_me_patch_updates_a_single_field(self):
        self.client.force_login(self.user)

        response = self.client.patch(
            '/api/custom-reg-form/v1/me/',
            data=json.dumps({'zipcode': '12345'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.content)
        self.assertEqual(payload['zipcode'], '12345')
        self.assertTrue(ExtraInfo.objects.filter(user=self.user).exists())
        self.assertEqual(ExtraInfo.objects.get(user=self.user).zipcode, '12345')

    def test_me_patch_returns_field_level_validation_errors(self):
        self.client.force_login(self.user)

        response = self.client.patch(
            '/api/custom-reg-form/v1/me/',
            data=json.dumps({'zipcode': 'not-a-zip'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        payload = json.loads(response.content)
        self.assertIn('zipcode', payload)
        self.assertIn('Must be a valid zipcode', payload['zipcode'])

    @override_settings(REGISTRATION_EXTRA_FIELDS={
        'ethnicity': 'required',
        'employment_status': 'optional',
        'enrolled_in_school': 'hidden',
        'country': 'required',
    })
    def test_metadata_exposes_custom_field_visibility(self):
        self.client.force_login(self.user)

        response = self.client.get('/api/custom-reg-form/v1/me/')

        self.assertEqual(response.status_code, 200)
        visibility = json.loads(response.content)['metadata']['visibility']
        self.assertEqual(visibility['ethnicity'], 'required')
        self.assertEqual(visibility['employment_status'], 'optional')
        self.assertEqual(visibility['enrolled_in_school'], 'hidden')
        self.assertEqual(set(visibility), set(self.FIELD_NAMES))
        self.assertNotIn('country', visibility)

    @override_settings(REGISTRATION_EXTRA_FIELDS={})
    def test_missing_visibility_configuration_defaults_to_optional(self):
        self.client.force_login(self.user)

        response = self.client.get('/api/custom-reg-form/v1/me/')

        visibility = json.loads(response.content)['metadata']['visibility']
        self.assertEqual(set(visibility.values()), {'optional'})


class UsernameApiAuthorizationTests(TestCase):
    """Tests for username-based custom account field authorization."""

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='alice', password='secret')
        self.other_user = user_model.objects.create_user(username='bob', password='secret')
        self.staff_user = user_model.objects.create_user(
            username='staff', password='secret', is_staff=True,
        )

    def url_for(self, username):
        return f'/api/custom-reg-form/v1/accounts/{username}/'

    def test_username_route_requires_authentication(self):
        response = self.client.get(self.url_for(self.user.username))

        self.assertEqual(response.status_code, 401)

    def test_self_access_reads_and_updates(self):
        self.client.force_login(self.user)

        get_response = self.client.get(self.url_for(self.user.username))
        patch_response = self.client.patch(
            self.url_for(self.user.username),
            data=json.dumps({'zipcode': '12345'}),
            content_type='application/json',
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(json.loads(patch_response.content)['zipcode'], '12345')

    def test_staff_can_read_another_user(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url_for(self.user.username))

        self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_read_another_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url_for(self.other_user.username))

        self.assertEqual(response.status_code, 403)

    def test_cross_user_updates_are_rejected(self):
        self.client.force_login(self.staff_user)

        response = self.client.patch(
            self.url_for(self.user.username),
            data=json.dumps({'zipcode': '12345'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(ExtraInfo.objects.filter(user=self.user).exists())
