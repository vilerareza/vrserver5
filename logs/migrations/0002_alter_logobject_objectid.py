# Generated by Django 3.2.3 on 2022-08-01 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logobject',
            name='objectID',
            field=models.IntegerField(),
        ),
    ]
