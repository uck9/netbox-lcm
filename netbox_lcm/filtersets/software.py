import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models.software import SoftwareProduct, SoftwareRelease, \
    SoftwareReleaseAssignment


__all__ = (
    'SoftwareProductFilterSet',
    'SoftwareReleaseFilterSet',
    'SoftwareReleaseAssignmentFilterSet',
)


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

class SoftwareReleaseFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareRelease
        fields = (
            'product', 'version', 'device_type', 'device_role',
        )

class SoftwareReleaseAssignmentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareReleaseAssignment
        fields = (
            'device', 'release', 'currently_active',
        )