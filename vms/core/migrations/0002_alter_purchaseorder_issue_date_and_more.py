# Generated by Django 4.2.11 on 2024-05-01 07:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="order_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="average_response_time",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="fulfillment_rate",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="on_time_delivery_rate",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="quality_rating_avg",
            field=models.FloatField(default=0),
        ),
    ]
