# Generated by Django 4.0.4 on 2022-05-20 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_errorreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorreport',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='signup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
