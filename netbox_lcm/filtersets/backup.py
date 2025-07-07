import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models import DeviceBackupPolicy, DeviceBackupResult

__all__ = (
    'DeviceBackupPolicyFilterSet',
    'DeviceBackupResultFilterSe',
)

class DeviceBackupPolicyFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = DeviceBackupPolicy
        fields = ['device', 'enabled', 'evaluate_status', 'backup_system']

class DeviceBackupResultFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = DeviceBackupResult
        fields = ['policy', 'status', 'backup_date']