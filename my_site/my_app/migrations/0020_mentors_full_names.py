# Generated by Django 3.0.6 on 2020-06-06 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0019_auto_20200606_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentors',
            name='full_names',
            field=models.CharField(default='user', max_length=100),
        ),
    ]
