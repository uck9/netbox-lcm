import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q

from dcim.models import DeviceType, Manufacturer
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models.software import DeviceTypeFamily, SoftwareProduct, SoftwareRelease, \
    SoftwareReleaseAssignment


__all__ = (
    'DeviceTypeFamilyFilterSet',
    'SoftwareProductFilterSet',
    'SoftwareReleaseFilterSet',
    'SoftwareReleaseAssignmentFilterSet',
)
class DeviceTypeFamilyFilterSet(NetBoxModelFilterSet):
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all()
    )
    device_types = django_filters.ModelMultipleChoiceFilter(
        field_name='device_types',
        queryset=DeviceType.objects.all(),
        label='Device Types',
    )

    class Meta:
        model = DeviceTypeFamily
        fields = ['name', 'manufacturer', 'device_types']

class SoftwareReleaseFilterSet(NetBoxModelFilterSet):
    devicetype_family = django_filters.ModelChoiceFilter(
        queryset=DeviceTypeFamily.objects.all()
    )

    class Meta:
        model = SoftwareRelease
        fields = ['product', 'devicetype_family', 'version', 'device_role','status']


class SoftwareProductFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareProduct
        fields = fields = [
            'name',
            'platform',
            'major_version',
            'minor_version',
            'alias',
            'release_date',
            'end_of_security_date',
            'end_of_support_date',
        ]

class SoftwareReleaseAssignmentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareReleaseAssignment
        fields = (
            'device', 'release', 'currently_active',
        )