# Generated by Django 3.0.4 on 2020-08-16 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_seedproduct_related_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2),
        ),
    ]
