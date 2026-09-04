import json

from django.contrib.auth import get_user_model
from django.test import TestCase

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
