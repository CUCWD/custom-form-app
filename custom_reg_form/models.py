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
    ETHNIC_GROUPS = (
        ('w', ugettext_noop('White')),
        ('hl', ugettext_noop('Hispanic or Latino')),
        ('ba', ugettext_noop('Black or African American')),
        ('na', ugettext_noop('Native American or American Indian')),
        ('api', ugettext_noop('Asian / Pacific Islander')),
        ('other', ugettext_noop('Other'))
    )
    ethnicity = models.CharField(
        verbose_name="Ethnicity",
        blank=True, null=True, max_length=6, db_index=True,
        choices=ETHNIC_GROUPS
    )

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


