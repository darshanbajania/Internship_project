# Generated by Django 3.0.6 on 2020-06-10 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0027_proposal_mentor_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='summary',
            field=models.CharField(default='no summary', max_length=2000),
        ),
    ]