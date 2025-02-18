from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lcm.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleTable',
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
            'id', 'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance', 'end_of_security', 'end_of_support',
            'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'name', 'assigned_object', 'end_of_sale', 'end_of_maintenance'
        )
