# Generated by Django 5.2 on 2025-04-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_profile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=10000.0, max_digits=15),
        ),
    ]
