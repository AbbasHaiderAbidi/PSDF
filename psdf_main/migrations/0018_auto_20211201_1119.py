# Generated by Django 3.2.5 on 2021-12-01 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0017_auto_20211201_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boqdata',
            name='itemqty',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='boqdata',
            name='unitcost',
            field=models.TextField(null=True),
        ),
    ]
