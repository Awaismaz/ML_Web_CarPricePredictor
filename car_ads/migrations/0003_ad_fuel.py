# Generated by Django 4.1.7 on 2023-03-12 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_ads", "0002_remove_ad_first_hand_ad_fh_alter_ad_fiscal_power_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ad",
            name="fuel",
            field=models.CharField(default="", max_length=200),
        ),
    ]
