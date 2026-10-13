"""Tests for custom registration form fields and persistence."""

from django.test import TestCase

from custom_reg_form.forms import ExtraInfoForm


class ExtraInfoTest(TestCase):
    """Validate custom registration form behavior."""

    def test_extra_info_form(self):
        """Expose the expected registration field labels."""
        form = ExtraInfoForm()
        self.assertEqual(form.fields['ethnicity'].label, 'Race or Ethnicity')
        self.assertEqual(form.fields['zipcode'].label, 'Zip Code')
        self.assertEqual(form.fields['employment_status'].label, 'Employment Status')

    def test_extra_form_handler(self):
        """Accept valid custom registration data."""
        form_data = {"ethnicity": "w", "zipcode": "29631", "employment_status": "selfemployed"}
        form = ExtraInfoForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_extra_form_submit(self):
        """Persist validated custom registration fields."""
        form_data = {"ethnicity": "w", "zipcode": "29631", "employment_status": "selfemployed"}
        form = ExtraInfoForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        record = form.save()
        record.refresh_from_db()
        for field, value in form_data.items():
            self.assertEqual(getattr(record, field), value)
