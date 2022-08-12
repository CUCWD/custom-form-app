from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_noop
from django.core.validators import RegexValidator
# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True, on_delete=models.CASCADE)

    def __enumerable_to_display(self, enumerables, enum_value):
        """ Get the human readable value from an enumerable list of key-value pairs. """
        return dict(enumerables)[enum_value]

    ETHNIC_GROUPS = (
        ('w', ugettext_noop('White')),
        ('hl', ugettext_noop('Hispanic or Latino/a')),
        ('ba', ugettext_noop('Black or African American')),
        ('na', ugettext_noop('American Indian or Alaska Native')),
        
        # ('api', ugettext_noop('Asian / Pacific Islander')),

        ('as', ugettext_noop('Asian')),
        ('nhpi', ugettext_noop('Native Hawaiian or Pacific Islander')),
        ('me', ugettext_noop('Middle Eastern')),
        ('bm', ugettext_noop('Biracial or Multiracial')),
        ('other', ugettext_noop('Other')), # change this to text field
        ('prefer-not-to-say', ugettext_noop('Prefer not to say'))
    )
    ethnicity = models.CharField(
        verbose_name="Ethnicity",
        blank=True, null=True, max_length=25, db_index=True,
        choices=ETHNIC_GROUPS
    )

    @property
    def ethnicity_display(self):
        """ Convenience method that returns the human readable ethnicity. """
        if self.ethnicity:
            return self.__enumerable_to_display(self.ETHNIC_GROUPS, self.ethnicity)

    EMPLOYMENT_STATUS_CHOICES = (
        ('efw', ugettext_noop('Employed for wages')),
        ('selfemployed', ugettext_noop('Self-employed')),
        ('student', ugettext_noop('Student')),
        ('homemaker', ugettext_noop('Homemaker')),
        ('oowlfw', ugettext_noop('Out of work and looking for work')),
        ('oownclfw', ugettext_noop('Out of work but not currently looking for work')),
        ('military', ugettext_noop('Military')),
        ('retired', ugettext_noop('Retired')),
        ('utw', ugettext_noop('Unable to work')),
        ('other', ugettext_noop('Other')),

    )
    employment_status = models.CharField(
        verbose_name="Employment Status",
        blank=True, null=True, max_length=20, db_index=True,
        choices=EMPLOYMENT_STATUS_CHOICES
    )

    @property
    def employment_status_display(self):
        """ Convenience method that returns the human readable gender. """
        if self.employment_status:
            return self.__enumerable_to_display(self.EMPLOYMENT_STATUS_CHOICES, self.employment_status)

    zipcode = models.CharField(
        verbose_name="Zip Code",
        max_length=10,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r'^(\d{5}([\-]\d{4})?)$',
            message=u'Must be a valid zipcode'
        )]
    )

    ENROLLED_IN_SCHOOL_CHOICES = (
        ('no', ugettext_noop('No')),
        ('yes', ugettext_noop('Yes')),
        ('prefer-not-to-say', ugettext_noop('Prefer not to say'))
    )

    enrolled_in_school = models.CharField(
        verbose_name="Are you currently enrolled in school?",
        max_length=25,
        null=True,
        blank=True,
        choices=ENROLLED_IN_SCHOOL_CHOICES
    )

    @property
    def enrolled_in_school_display(self):
        """ Convenience method that returns the human readable gender. """
        if self.enrolled_in_school:
            return self.__enumerable_to_display(self.ENROLLED_IN_SCHOOL_CHOICES, self.enrolled_in_school)

    ENROLLED_IN_SCHOOL_TYPE_CHOICES = (
        ('hs', ugettext_noop('High School or GED')),
        ('two-year', ugettext_noop('2-year degree')),
        ('four-year', ugettext_noop('4-year degree')),
        ('grad', ugettext_noop('Graduate School')),
        ('o', ugettext_noop('Other')),
        ('prefer-not-to-say', ugettext_noop('Prefer not to say'))
    )
    enrolled_in_school_type = models.CharField(
        verbose_name="Enrolled in school type",
        max_length=25,
        null=True,
        blank=True,
        choices=ENROLLED_IN_SCHOOL_TYPE_CHOICES
    )

    @property
    def enrolled_in_school_type_display(self):
        """ Convenience method that returns the human readable gender. """
        if self.enrolled_in_school_type:
            return self.__enumerable_to_display(self.ENROLLED_IN_SCHOOL_TYPE_CHOICES, self.enrolled_in_school_type)

    LOCAL_COMMUNITY_LIVING_CHOICES = (
        ('ls',ugettext_noop('A large city')),
        ('su',ugettext_noop('A suburb near a large city')),
        ('ra',ugettext_noop('A rural area')),
        ('prefer-not-to-say', ugettext_noop('Prefer not to say'))
    )
    local_community_living = models.CharField(
        verbose_name="Local Community Living",
        max_length=25,
        null=True,
        blank=True,
        choices=LOCAL_COMMUNITY_LIVING_CHOICES
    )

    @property
    def local_community_living_display(self):
        """ Convenience method that returns the human readable gender. """
        if self.local_community_living:
            return self.__enumerable_to_display(self.LOCAL_COMMUNITY_LIVING_CHOICES, self.local_community_living)


