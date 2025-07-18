from django.utils.translation import gettext as _

import django_tables2 as tables

from netbox.tables import columns, NetBoxTable, ChoiceFieldColumn
from netbox_lcm.models import SupportContract, Vendor, SupportContractAssignment, SupportSKU

__all__ = (
    'VendorTable',
    'SupportSKUTable',
    'SupportContractTable',
    'SupportContractAssignmentTable'
)


class VendorTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        verbose_name=_('Name')
    )

    class Meta(NetBoxTable.Meta):
        model = Vendor
        fields = (
            'id', 'pk', 'name',
        )
        default_columns = (
            'id', 'pk', 'name',
        )


class SupportSKUTable(NetBoxTable):
    sku = tables.Column(
        verbose_name=_('SKU'),
        linkify=True,
    )
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = SupportSKU
        fields = (
            'id', 'pk', 'manufacturer', 'sku', 'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'manufacturer', 'sku',
        )


class SupportContractTable(NetBoxTable):
    contract_id = tables.Column(
        linkify=True,
        verbose_name=_('Contract ID')
    )

    class Meta(NetBoxTable.Meta):
        model = SupportContract
        fields = (
            'id', 'pk', 'contract_id', 'start', 'renewal', 'end', 'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'contract_id',
        )


class SupportContractAssignmentTable(NetBoxTable):
    contract = tables.Column(
        verbose_name=_('Contract'),
        linkify=True,
    )
    sku = tables.Column(
        verbose_name=_('SKU'),
        linkify=True,
    )
    device_name = tables.Column(
        verbose_name=_('Device Name'),
        accessor='device__name',
        linkify=True,
        orderable=True,
    )
    device_serial = tables.Column(
        verbose_name=_('Serial Number'),
        accessor='device__serial',
        orderable=True,
    )
    device_model = tables.Column(
        verbose_name=_('Device Model'),
        accessor='device__device_type__model',
        linkify=False,
        orderable=True,
    )
    device_status = ChoiceFieldColumn(
        verbose_name=_('Device Status'),
        accessor='device__status',
        orderable=True,
    )
    support_coverage_status = ChoiceFieldColumn()
    license_name = tables.Column(
        verbose_name=_('License'),
        accessor='license__license__name',
        linkify=False,
        orderable=True,
    )
    quantity = tables.Column(
        verbose_name=_('License Quantity'),
        accessor='license__quantity',
        orderable=False,
    )
    renewal = tables.Column(
        verbose_name=_('Renewal Date'),
        accessor='contract__renewal',
    )
    end = tables.Column(
        verbose_name=_('End Date'),
        accessor='end_date',
        orderable=False,
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = SupportContractAssignment
        fields = (
            'id', 'pk', 'contract', 'sku', 'device_name', 'license_name', 'device_model', 'device_serial', 'support_coverage_status', 'quantity',
            'renewal', 'end', 'tags', 'description', 'comments',
        )
        default_columns = (
            'id', 'pk', 'contract', 'sku', 'device_name', 'license_name', 'device_model', 'device_serial', 'end', 'tags'
        )
