# Generated by Django 3.2.5 on 2021-11-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0011_projects_completedate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='ext1',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='ext2',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='ext3',
        ),
        migrations.AddField(
            model_name='projects',
            name='ext',
            field=models.TextField(null=True),
        ),
    ]