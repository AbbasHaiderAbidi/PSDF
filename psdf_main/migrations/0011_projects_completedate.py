# Generated by Django 3.2.5 on 2021-11-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0010_projects_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='completedate',
            field=models.DateField(null=True),
        ),
    ]
