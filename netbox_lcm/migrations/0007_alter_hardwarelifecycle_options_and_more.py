# Generated by Django 4.1.7 on 2023-05-12 14:06

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0171_cabletermination_change_logging'),
        ('netbox_lcm', '0006_alter_supportcontractassignment_assigned_object_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hardwarelifecycle',
            options={'ordering': ['assigned_object_type']},
        ),
        migrations.AddField(
            model_name='supportcontractassignment',
            name='end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='dcim.manufacturer'),
        ),
        migrations.AlterField(
            model_name='licenseassignment',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='dcim.device'),
        ),
        migrations.AlterField(
            model_name='licenseassignment',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='netbox_lcm.license'),
        ),
        migrations.AlterField(
            model_name='licenseassignment',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='netbox_lcm.vendor'),
        ),
        migrations.AlterField(
            model_name='supportcontract',
            name='end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supportcontract',
            name='renewal',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supportcontract',
            name='start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supportcontract',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to='netbox_lcm.vendor'),
        ),
        migrations.AlterField(
            model_name='supportcontractassignment',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='netbox_lcm.supportcontract'),
        ),
        migrations.AlterField(
            model_name='supportcontractassignment',
            name='sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='netbox_lcm.supportsku'),
        ),
        migrations.AlterField(
            model_name='supportsku',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='dcim.manufacturer'),
        ),
        migrations.AddConstraint(
            model_name='hardwarelifecycle',
            constraint=models.UniqueConstraint(models.F('assigned_object_type'), models.F('assigned_object_id'), name='netbox_lcm_hardwarelifecycle_unique_object', violation_error_message='Objects must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='license',
            constraint=models.UniqueConstraint(models.F('manufacturer'), django.db.models.functions.text.Lower('name'), name='netbox_lcm_license_unique_manufacturer_name', violation_error_message='SKU name must be unique per manufacturer.'),
        ),
        migrations.AddConstraint(
            model_name='licenseassignment',
            constraint=models.UniqueConstraint(models.F('license'), models.F('vendor'), models.F('device'), name='netbox_lcm_licenseassignment_unique_license_vendor_device', violation_error_message='License assignment must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='supportcontract',
            constraint=models.UniqueConstraint(models.F('vendor'), django.db.models.functions.text.Lower('contract_id'), name='netbox_lcm_supportcontract_unique_vendor_contract_id', violation_error_message='Contract must be unique per vendor.'),
        ),
        migrations.AddConstraint(
            model_name='supportcontractassignment',
            constraint=models.UniqueConstraint(models.F('contract'), models.F('sku'), models.F('assigned_object_type'), models.F('assigned_object_id'), name='netbox_lcm_supportcontractassignment_unique_assignments', violation_error_message='Contract assignments must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='supportcontractassignment',
            constraint=models.UniqueConstraint(models.F('contract'), models.F('assigned_object_type'), models.F('assigned_object_id'), condition=models.Q(('sku__isnull', True)), name='netbox_lcm_supportcontractassignment_unique_assignment_null_sku', violation_error_message='Contract assignments to assigned_objects must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='supportsku',
            constraint=models.UniqueConstraint(models.F('manufacturer'), django.db.models.functions.text.Lower('sku'), name='netbox_lcm_supportsku_unique_manufacturer_sku', violation_error_message='SKU must be unique per manufacturer.'),
        ),
        migrations.AddConstraint(
            model_name='vendor',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='netbox_lcm_vendor_unique_name', violation_error_message='Vendor must be unique.'),
        ),
    ]
