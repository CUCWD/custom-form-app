from .models import ExtraInfo
from django.forms import ModelForm


class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['ethnicity'].error_messages = {
            "required": u"Please tell us your ethnicity",
            "invalid": u"Enter correct ethnicity",
        }
        self.fields['ethnicity_free_input'].error_messages = {
            "required": u"Please specify your ethnicity",
            "invalid": u"Enter correct ethnicity",
        }
        self.fields['employment_status'].error_messages = {
            "required": u"Please tell us your employment status",
            "invalid": u"Enter correct employment status",
        }
        self.fields['zipcode'].error_messages = {
            "required": u"Please tell us your American ZIP Code",
            "invalid": u"Invalid American Postal Code (nnnnn or nnnnn-nnnn)",
        }
        self.fields['enrolled_in_school'].error_messages = {
            "required": u"Please tell us if you are enrolled in school",
            "invalid": u"Enter correct school enrollment status",
        }
        self.fields['enrolled_in_school_type'].error_messages = {
            "required": u"Please tell us about the type of school you are enrolled in",
            "invalid": u"Enter correct school enrollment type",
        }
        self.fields['local_community_living'].error_messages = {
            "required": u"Please tell us which of the following best describes the place you live now",
            "invalid": u"Enter correct local community type",
        }
        self.fields['gender_free_input'].error_messages = {
            "required": u"Please specify your Gender",
            "invalid": u"Enter correct Gender",
        }


    class Meta(object):
        model = ExtraInfo
        fields = ('gender_free_input','ethnicity','ethnicity_free_input','employment_status','zipcode', 'enrolled_in_school', 'enrolled_in_school_type', 'local_community_living')
