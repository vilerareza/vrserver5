# Generated by Django 3.2.3 on 2022-08-24 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20220824_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='showName',
        ),
        migrations.AddField(
            model_name='device',
            name='hostName',
            field=models.CharField(default='hostname', max_length=50),
        ),
    ]