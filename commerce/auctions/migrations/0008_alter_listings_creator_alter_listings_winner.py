# Generated by Django 4.0.1 on 2022-02-05 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_delete_bids_listings_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
