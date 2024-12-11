# Generated by Django 5.0.9 on 2024-10-13 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_lcm', '0013_fix_hardware_lifecycle_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hardwarelifecycle',
            old_name='last_contract_date',
            new_name='last_contract_attach',
        ),
        migrations.AddField(
            model_name='hardwarelifecycle',
            name='last_contract_renewal',
            field=models.DateField(blank=True, null=True),
        ),
    ]