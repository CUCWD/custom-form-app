from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('custom_reg_form', '0011_auto_20220812_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='enrolled_in_school_type',
            field=models.CharField(blank=True, choices=[('hs', 'High School'), ('two-year', '2-year/technical college'), ('four-year', '4-year college or university'), ('grad', 'Graduate School'), ('prefer-not-to-say', 'Prefer not to say')], max_length=25, null=True, verbose_name='Type of Current School Enrollment'),
        ),
        migrations.AlterField(
            model_name='extrainfo',
            name='ethnicity',
            field=models.CharField(blank=True, choices=[('w', 'White'), ('ba', 'Black or African American'), ('na', 'American Indian or Alaska Native'), ('as', 'Asian'), ('nhpi', 'Native Hawaiian or Pacific Islander'), ('hl', 'Hispanic or Lanito/a'), ('me', 'Middle Eastern'), ('bm', 'Biracial or Multiracial'), ('o', 'Other'), ('prefer-not-to-say', 'Prefer not to say')], db_index=True, max_length=25, null=True, verbose_name='Race or Ethnicity'),
        ),
    ]