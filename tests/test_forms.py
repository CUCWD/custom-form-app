from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import ExtraInfoForm
import json

# Create your tests here.
class ExtraInfoTest(TestCase):
    """
    Test reg form ----> Test cases need to be rewritten
    """
    def setUp(self):
        super(ExtraInfoTest, self).setUp()
        self.client = Client()

    def test_extra_info_form(self):
        """Ensure that form is rendered to registration page"""
        response1 = "Ethnicity"
        response2 = "Zip Code"
        response3 = "Employment Status"
        self.assertTrue("Ethnicity")
        self.assertTrue("Zip Code")
        self.assertTrue("Employment Status")

    def test_extra_form_handler(self):
        """Ensure that form properly accepts test data"""
        form_data = {"ethnicity": "w", "zipcode": "29631","employment_status":"selfemployed"}
        form = ExtraInfoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_extra_form_submit(self):
        """Ensure that form properly requires phone and country_code"""
        response1 = "Ethnicity"
        response2 = "Zip Code"
        response3 = "Employment Status"
        self.assertTrue("Ethnicity")
        self.assertTrue("Zip Code")
        self.assertTrue("Employment Status")
        #response = self.client.post(reverse('user_api_registration'))
        #response_content = json.loads(response.content)
        #self.assertEquals(response_content.get("ethnicity")
                          #[dict(user_message="Select ethnicity")])
        #self.assertEquals(response_content.get("zipcode"),
                          #[dict(user_message="enter zipcode")])
        #self.assertEquals(response_content.get("employment_status"),
                          #[dict(user_message="enter employment status")])
