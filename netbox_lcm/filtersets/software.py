import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q

from dcim.models import DeviceRole, DeviceType, Manufacturer
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models.software import (
    DeviceTypeFamily, 
    SoftwareProduct,
    SoftwareRelease,
    SoftwareReleaseCompatibility, 
    SoftwareReleaseAssignment,
    SoftwareReleaseCompatibilityStatus
)


__all__ = (
    'DeviceTypeFamilyFilterSet',
    'SoftwareProductFilterSet',
    'SoftwareReleaseFilterSet',
    'SoftwareReleaseCompatibilityFilterSet',
    'SoftwareReleaseCompatibilityStatusFilterSet',
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
    class Meta:
        model = SoftwareRelease
        fields = ['product', 'version']


class SoftwareReleaseCompatibilityFilterSet(NetBoxModelFilterSet):
    devicetype_family = django_filters.ModelChoiceFilter(
        queryset=DeviceTypeFamily.objects.all()
    )

    class Meta:
        model = SoftwareReleaseCompatibility
        fields = ['software_release', 'devicetype_family']


class SoftwareProductFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareProduct
        fields = [
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
    is_active = django_filters.BooleanFilter(
        method='filter_is_active',
        label='Active Assignment',
        widget=django_filters.widgets.BooleanWidget(),
        initial=True  # Important for defaulting in form
    )

    def filter_is_active(self, queryset, name, value):
        if value is True:
            return queryset.filter(unassigned_on__isnull=True)
        elif value is False:
            return queryset.filter(unassigned_on__isnull=False)
        return queryset

    class Meta:
        model = SoftwareReleaseAssignment
        fields = (
            'device', 'release', 'assigned_on', 'is_active'
        )


class SoftwareReleaseCompatibilityStatusFilterSet(NetBoxModelFilterSet):
    compatibility_id = django_filters.ModelChoiceFilter(
        queryset=SoftwareReleaseCompatibilityStatus.objects.all(),
        field_name='compatibility__id',
        label='Compatibility'
    )
    device_role_id = django_filters.ModelChoiceFilter(
        queryset=DeviceRole.objects.all(),
        field_name='device_role__id',
        label='Device Role'
    )

    class Meta:
        model = SoftwareReleaseCompatibilityStatus
        fields = ['compatibility_id', 'device_role_id', 'status']