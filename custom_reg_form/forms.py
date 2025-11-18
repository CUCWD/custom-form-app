from .models import ExtraInfo
from django.forms import ModelForm


class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)


        # Ethnicity
        # ----------------------------------

        # Remove the Django serialized default of '---------' from the choices
        field = self.fields['ethnicity']
        # Keep it optional, but change the placeholder text
        choices = list(field.choices)
        if choices and choices[0][0] == "":
            choices.remove(choices[0])
        field.choices = choices

        # This is where the error on the `frontend_app_authn` MFE registration form
        # was causing the page to crash. Previously we had set this to an object.
        # It just wants a string of dict of strings now.
        self.fields['ethnicity'].error_messages = u"Select your ethnicity"


        # Employment Status
        # ----------------------------------

        # Remove the Django serialized default of '---------' from the choices
        field = self.fields['employment_status']
        # Keep it optional, but change the placeholder text
        choices = list(field.choices)
        if choices and choices[0][0] == "":
            choices.remove(choices[0])
        field.choices = choices

        # This is where the error on the `frontend_app_authn` MFE registration form
        # was causing the page to crash. Previously we had set this to an object.
        # It just wants a string of dict of strings now.
        self.fields['employment_status'].error_messages = u"Select your employment status"
        
        # ZIP Code
        # ----------------------------------
        self.fields['zipcode'].error_messages = u"Please tell us your American ZIP Code"

        # Enrolled in School
        # ----------------------------------

        # Remove the Django serialized default of '---------' from the choices
        field = self.fields['enrolled_in_school']
        # Keep it optional, but change the placeholder text
        choices = list(field.choices)
        if choices and choices[0][0] == "":
            choices.remove(choices[0])
        field.choices = choices

        # This is where the error on the `frontend_app_authn` MFE registration form
        # was causing the page to crash. Previously we had set this to an object.
        # It just wants a string of dict of strings now.
        self.fields['enrolled_in_school'].error_messages = u"Select your enrolled in school status"
        
        # Enrolled in School Type
        # ----------------------------------

        # Remove the Django serialized default of '---------' from the choices
        field = self.fields['enrolled_in_school_type']
        # Keep it optional, but change the placeholder text
        choices = list(field.choices)
        if choices and choices[0][0] == "":
            choices.remove(choices[0])
        field.choices = choices

        # This is where the error on the `frontend_app_authn` MFE registration form
        # was causing the page to crash. Previously we had set this to an object.
        # It just wants a string of dict of strings now.
        self.fields['enrolled_in_school_type'].error_messages = u"Select the type of school you are enrolled in"
        
        # Local Community Living
        # ----------------------------------

        # Remove the Django serialized default of '---------' from the choices
        field = self.fields['local_community_living']
        # Keep it optional, but change the placeholder text
        choices = list(field.choices)
        if choices and choices[0][0] == "":
            choices.remove(choices[0])
        field.choices = choices

        # This is where the error on the `frontend_app_authn` MFE registration form
        # was causing the page to crash. Previously we had set this to an object.
        # It just wants a string of dict of strings now.
        self.fields['local_community_living'].error_messages = u"Select the place that describes where you live now"

    class Meta(object):
        model = ExtraInfo
        fields = ('ethnicity','employment_status','zipcode', 'enrolled_in_school', 'enrolled_in_school_type', 'local_community_living')
