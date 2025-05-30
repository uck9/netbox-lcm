# Generated by Django 5.1.5 on 2025-05-04 06:55

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0200_populate_mac_addresses'),
        ('extras', '0122_charfield_null_choices'),
        ('netbox_lcm', '0016_alter_supportcontractassignment_license_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HardwareLifecyclePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('plan_type', models.CharField(default='to_review', max_length=20)),
                ('status', models.CharField(default='to_review', max_length=20)),
                ('resourcing_type', models.CharField(default='to_review', max_length=20)),
                ('completion_by', models.DateField(blank=True, null=True)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='device', to='dcim.device')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ['plan_type'],
            },
        ),
    ]
