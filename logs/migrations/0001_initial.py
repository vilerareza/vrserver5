# Generated by Django 3.2.3 on 2022-08-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectID', models.IntegerField(max_length=5)),
                ('timeStamp', models.CharField(blank=True, max_length=30)),
                ('faceData', models.CharField(blank=True, max_length=250000)),
            ],
        ),
    ]