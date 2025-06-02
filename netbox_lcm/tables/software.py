from django.utils.translation import gettext as _
import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from netbox_lcm.models import DeviceTypeFamily, SoftwareProduct, SoftwareRelease, \
    SoftwareReleaseAssignment


__all__ = (
    'DeviceTypeFamilyTable',
    'SoftwareProductTable',
    'SoftwareReleaseTable',
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
            'name',
            'manufacturer',
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
            'name',
            'manufacturer',
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
    device_type_family = tables.Column(linkify=True)
    device_role = tables.Column(linkify=True)
    version = tables.Column()
    status = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = SoftwareRelease
        fields = ('product', 'version', 'device_type_family', 'device_role', 'status')

class SoftwareReleaseAssignmentTable(NetBoxTable):
    device = tables.Column(linkify=True)
    release = tables.Column(linkify=True)
    currently_active = tables.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = SoftwareReleaseAssignment
        fields = ('id', 'device', 'release', 'assigned', 'currently_active')
