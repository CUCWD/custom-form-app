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
        self.fields['employment_status'].error_messages = {
            "required": u"Please tell us your employment status",
            "invalid": u"Enter correct employment status",
        }
        self.fields['zipcode'].error_messages = {
            "required": u"Please tell us your American ZIP Code",
            "invalid": u"Invalid American Postal Code (nnnn or nnnnn-nnnn)",
        }


    class Meta(object):
        model = ExtraInfo
        fields = ('ethnicity','employment_status','zipcode')
