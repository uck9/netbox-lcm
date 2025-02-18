from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_lcm.models import License, LicenseAssignment


__all__ = (
    'LicenseTable',
    'LicenseAssignmentTable',
)


class LicenseTable(NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True,
    )
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            'id', 'pk', 'name', 'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'name',
        )


class LicenseAssignmentTable(NetBoxTable):
    license = tables.Column(
        verbose_name=_('License'),
        linkify=True
    )
    vendor = tables.Column(
        verbose_name=_('Vendor'),
        linkify=True
    )
    device = tables.Column(
        verbose_name=_('Device'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            'id', 'pk', 'license', 'vendor', 'device', 'quantity', 'start', 'end','description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'license', 'vendor', 'device', 'quantity', 'end',
        )
