# Generated by Django 3.2.5 on 2021-11-30 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0013_projects_extf'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='amt_updated',
            field=models.IntegerField(null=True),
        ),
    ]
