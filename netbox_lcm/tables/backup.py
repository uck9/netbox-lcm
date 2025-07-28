# netbox_lcm/tables.py

import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, BooleanColumn
from dcim.models import Device

from netbox_lcm.models import DeviceBackupPolicy, DeviceBackupResult
from netbox_lcm.choices import BackupSystemChoices, BackupStatusChoices


__all__ = (
    'DeviceBackupPolicyTable',
    'DeviceBackupResultTable',
)

#
# DeviceBackupPolicy Table
#

class DeviceBackupPolicyTable(NetBoxTable):
    device = tables.Column(linkify=True)
    enabled = BooleanColumn()
    critical = BooleanColumn()
    evaluate_status = BooleanColumn(verbose_name='Evaluate?')
    backup_system = ChoiceFieldColumn()
    destination = tables.Column()
    method = tables.Column()
    get_backup_health_score = tables.Column(verbose_name='Health Score')

    class Meta(NetBoxTable.Meta):
        model = DeviceBackupPolicy
        fields = (
            'id', 'device', 'enabled', 'critical', 'evaluate_status', 'backup_system',
            'destination', 'method', 'get_backup_health_score',
        )
        default_columns = ('id', 'device', 'enabled', 'backup_system', 'get_backup_health_score')


#
# DeviceBackupResult Table
#

class DeviceBackupResultTable(NetBoxTable):
    policy = tables.Column(linkify=True)
    device = tables.Column(accessor='policy.device', linkify=True, verbose_name='Device')
    backup_date = tables.DateColumn()
    status = ChoiceFieldColumn()
    backup_health_label = tables.TemplateColumn(
        template_code="""
        {% if record.backup_health_label == "Healthy" %}
            <span class="badge bg-success">Healthy</span>
        {% elif record.backup_health_label == "Warning" %}
            <span class="badge bg-warning">Warning</span>
        {% elif record.backup_health_label == "At Risk" %}
            <span class="badge bg-danger">At Risk</span>
        {% else %}
            <span class="badge bg-secondary">Excluded</span>
        {% endif %}
        """,
        verbose_name="Backup Health",
        orderable=False,
    )
    days_since_last_success = tables.Column(verbose_name="Days Since Last Success")

    class Meta(NetBoxTable.Meta):
        model = DeviceBackupResult
        fields = (
            'id', 'policy', 'device', 'backup_date', 'status',
            'backup_health_label', 'days_since_last_success',
        )
        default_columns = ('id', 'device', 'backup_date', 'status', 'backup_health_label')
