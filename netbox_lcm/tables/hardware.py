from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan


__all__ = (
    'HardwareLifecycleTable',
    'HardwareLifecyclePlanTable',
)


class HardwareLifecycleTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        accessor='name',
        orderable=False,
    )
    assigned_object = tables.Column(
        linkify=True,
        verbose_name=_('Hardware'),
        orderable=False,
    )
    assigned_object_count = tables.Column(
        verbose_name=_('Assigned Object Count'),
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = HardwareLifecycle
        fields = (
            'id', 'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance', 'end_of_security',
            'end_of_support', 'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance'
        )


class HardwareLifecyclePlanTable(NetBoxTable):
    device = tables.Column(
        linkify=True,
        verbose_name=_('Device'),
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = HardwareLifecyclePlan
        fields = (
            'id', 'pk', 'device', 'plan_type', 'status', 'resourcing_type', 'completion_by',
            'tags','description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'device', 'plan_type', 'completion_by',
        )
