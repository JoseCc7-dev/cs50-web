# Generated by Django 4.0.1 on 2022-02-06 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listings_creator_alter_listings_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='description',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='listings',
            name='imageurl',
            field=models.CharField(max_length=90),
        ),
    ]
