from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from netbox_lcm.models import DeviceTypeFamily, SoftwareProduct, SoftwareRelease, \
    SoftwareReleaseAssignment, SoftwareReleaseStatus


__all__ = (
    'DeviceTypeFamilyTable',
    'SoftwareProductTable',
    'SoftwareReleaseTable',
    'SoftwareReleaseStatusTable',
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

class SoftwareReleaseStatusTable(NetBoxTable):
    release = tables.Column(
        accessor='release.version',
        verbose_name='Release Version',
        linkify=True
    )
    device_role = tables.Column(linkify=True)
    status = ChoiceFieldColumn()
    devicetype_manufacturer = tables.Column(
        accessor='release.devicetype_family.manufacturer',
        verbose_name='Manufacturer'
    )
    devicetype_family = tables.Column(
        linkify=True,
        verbose_name='Device Type Family'
    )

    class Meta(NetBoxTable.Meta):
        model = SoftwareReleaseStatus
        fields = ('id', 'release', 'manufacturer', 'devicetype_family', 'device_role', 'status')

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
