from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from netbox_lcm.models import (
    DeviceTypeFamily,
    SoftwareProduct,
    SoftwareRelease,
    SoftwareReleaseAssignment,
    SoftwareReleaseCompatibility,
    SoftwareReleaseCompatibilityStatus,
)


__all__ = (
    'DeviceTypeFamilyTable',
    'SoftwareProductTable',
    'SoftwareReleaseTable',
    'SoftwareReleaseCompatibilityTable',
    'SoftwareReleaseCompatibilityStatusTable',
    'SoftwareReleaseAssignmentTable'
)

class DeviceTypeFamilyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    manufacturer = tables.Column(linkify=True)
    device_types = tables.ManyToManyColumn(accessor='device_types.all')

    class Meta(NetBoxTable.Meta):
        model = DeviceTypeFamily
        fields = ('name', 'manufacturer', 'device_types', 'description')

class SoftwareProductTable(NetBoxTable):
    manufacturer = tables.Column(
        accessor='platform.manufacturer',
        linkify=True,
        verbose_name='Manufacturer'
    )
    platform = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    major_version = tables.Column()
    minor_version = tables.Column()
    alias = tables.Column()
    release_date = tables.DateColumn()
    end_of_security_date = tables.DateColumn()
    end_of_support_date = tables.DateColumn()
    documentation_url = tables.URLColumn()

    class Meta(NetBoxTable.Meta):
        model = SoftwareProduct
        fields = (
            'id',
            'manufacturer',
            'name',
            'platform',
            'major_version',
            'minor_version',
            'alias',
            'release_date',
            'end_of_security_date',
            'end_of_support_date',
            'documentation_url',
        )
        default_volumns = (
            'id',
            'manufacturer',
            'name',
            'platform',
            'major_version',
            'minor_version',
            'alias',
            'release_date',
            'end_of_security_date',
            'end_of_support_date',
        )

class SoftwareReleaseTable(NetBoxTable):
    product = tables.Column(linkify=True)
    version = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = SoftwareRelease
        fields = ('id', 'product', 'version', 'status')

class SoftwareReleaseCompatibilityTable(NetBoxTable):
    software_release = tables.Column(
        verbose_name='Software Release Version',
        linkify=True
    )
    devicetype_manufacturer = tables.Column(
        accessor='devicetype_family.manufacturer',
        verbose_name='Manufacturer'
    )
    devicetype_family = tables.Column(
        linkify=True,
        verbose_name='Device Type Family'
    )

    class Meta(NetBoxTable.Meta):
        model = SoftwareReleaseCompatibility
        fields = ('id', 'devicetype_manufacturer', 'devicetype_family', 'software_release')

class SoftwareReleaseAssignmentTable(NetBoxTable):
    device = tables.Column(linkify=True)
    release = tables.Column(linkify=True)
    is_active = tables.Column(
        accessor='unassigned_on', 
        verbose_name='Active', 
        orderable=False
    )

    def render_is_active(self, record):
        return '✅' if record.unassigned_on is None else '❌'

    class Meta(NetBoxTable.Meta):
        model = SoftwareReleaseAssignment
        fields = ('id', 'device', 'release', 'assigned_on', 'is_active', 
            'unassigned_on'
        )


class SoftwareReleaseCompatibilityStatusTable(NetBoxTable):
    compatibility = tables.Column(
        linkify=True,
        verbose_name="Release Compatibility"
    )
    device_role = tables.Column(
        linkify=True,
        verbose_name="Device Role",
        accessor='device_role',
        default="Default"
    )
    status = ChoiceFieldColumn()  # Auto-renders color-coded badge if defined in choices

    class Meta(NetBoxTable.Meta):
        model = SoftwareReleaseCompatibilityStatus
        fields = (
            'id',
            'compatibility',
            'device_role',
            'status',
        )
        default_columns = (
            'compatibility',
            'device_role',
            'status',
        )
