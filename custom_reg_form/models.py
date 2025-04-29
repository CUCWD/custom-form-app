from django.conf import settings
from django.db import models
from django.utils.translation import gettext_noop
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

    # [08/12/2022] removed these, but leaving comment since there'll still be
    # `api` in the existing data in db. This option was split into two.
    # ('api', gettext_noop('Asian / Pacific Islander')),
    ETHNIC_GROUPS = (
        ('w', gettext_noop('White')),
        ('ba', gettext_noop('Black or African American')),
        ('na', gettext_noop('American Indian or Alaska Native')),
        ('as', gettext_noop('Asian')),
        ('nhpi', gettext_noop('Native Hawaiian or Pacific Islander')),
        ('hl', gettext_noop('Hispanic or Latino/a')),
        ('me', gettext_noop('Middle Eastern')),
        ('bm', gettext_noop('Biracial or Multiracial')),
        ('o', gettext_noop('Other')),
        # ('other', gettext_noop('Other')), # TODO - change this to text field
        ('prefer-not-to-say', gettext_noop('Prefer not to say'))
    )
    ethnicity = models.CharField(
        verbose_name="Race or Ethnicity",
        blank=True, null=True, max_length=25, db_index=True,
        choices=ETHNIC_GROUPS
    )

    @property
    def ethnicity_display(self):
        """ Convenience method that returns the human readable ethnicity. """
        if self.ethnicity:
            return self.__enumerable_to_display(self.ETHNIC_GROUPS, self.ethnicity)

    EMPLOYMENT_STATUS_CHOICES = (
        ('efw', gettext_noop('Employed for wages')),
        ('selfemployed', gettext_noop('Self-employed')),
        ('student', gettext_noop('Student')),
        ('homemaker', gettext_noop('Homemaker')),
        ('oowlfw', gettext_noop('Out of work and looking for work')),
        ('oownclfw', gettext_noop('Out of work but not currently looking for work')),
        ('military', gettext_noop('Military')),
        ('retired', gettext_noop('Retired')),
        ('utw', gettext_noop('Unable to work')),
        # ('other', gettext_noop('Other')), # TODO - change this to text field
        ('prefer-not-to-say', gettext_noop('Prefer not to say'))

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
        ('no', gettext_noop('No')),
        ('yes', gettext_noop('Yes')),
        ('prefer-not-to-say', gettext_noop('Prefer not to say'))
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
        ('hs', gettext_noop('High School')),
        ('two-year', gettext_noop('2-year/technical college')),
        ('four-year', gettext_noop('4-year college or university')),
        ('grad', gettext_noop('Graduate School')),
        ('ne', gettext_noop('Not Enrolled')),
        # ('o', gettext_noop('Other')),  # change this to text field input
        ('prefer-not-to-say', gettext_noop('Prefer not to say'))
    )
    enrolled_in_school_type = models.CharField(
        verbose_name="Type of Current School Enrollment",
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
        ('ls',gettext_noop('A large city')),
        ('su',gettext_noop('A suburb near a large city')),
        ('sct',gettext_noop('A small city or town')),
        ('ra',gettext_noop('A rural area')),
        ('prefer-not-to-say', gettext_noop('Prefer not to say'))
    )
    local_community_living = models.CharField(
        verbose_name="Thinking about your local community, which of the following best describes the place you live now?",
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


