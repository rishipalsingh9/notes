# Generated by Django 3.2.2 on 2021-06-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_name', models.CharField(max_length=200)),
                ('prop_name', models.CharField(max_length=200)),
                ('email_agent', models.EmailField(max_length=254)),
                ('agency_address', models.CharField(max_length=500)),
                ('contact_no', models.PositiveSmallIntegerField()),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_name', models.CharField(max_length=200)),
                ('no_of_nights', models.PositiveSmallIntegerField()),
                ('travel_date', models.DateField()),
                ('end_date', models.DateField()),
                ('detail_itinerary', models.FileField(blank=True, upload_to='')),
            ],
        ),
    ]
