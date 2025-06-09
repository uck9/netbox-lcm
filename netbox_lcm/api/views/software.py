from netbox.api.viewsets import NetBoxModelViewSet
from dcim.api.views import DeviceViewSet
from netbox_lcm.models import \
    DeviceTypeFamily, SoftwareProduct, SoftwareRelease, SoftwareReleaseCompatibility, SoftwareReleaseAssignment
from netbox_lcm.filtersets import (
    DeviceTypeFamilyFilterSet,
    SoftwareProductFilterSet,
    SoftwareReleaseFilterSet,
    SoftwareReleaseCompatibilityFilterSet,
    SoftwareReleaseAssignmentFilterSet,
)
from netbox_lcm.api.serializers import (
    DeviceTypeFamilySerializer,
    SoftwareProductSerializer,
    SoftwareReleaseSerializer,
    SoftwareReleaseCompatibilitySerializer,
    SoftwareReleaseAssignmentSerializer,
)

__all__ = (
    'DeviceTypeFamilyViewSet',
    'SoftwareProductViewSet',
    'SoftwareReleaseViewSet',
    'SoftwareReleaseCompatibilityViewSet',
    'SoftwareReleaseAssignmentViewSet',
)

class SoftwareProductViewSet(NetBoxModelViewSet):
    queryset = SoftwareProduct.objects.all()
    serializer_class = SoftwareProductSerializer
    filterset_class = SoftwareProductFilterSet

class SoftwareReleaseViewSet(NetBoxModelViewSet):
    queryset = SoftwareRelease.objects.all()
    serializer_class = SoftwareReleaseSerializer
    filterset_class = SoftwareReleaseFilterSet

class SoftwareReleaseAssignmentViewSet(NetBoxModelViewSet):
    queryset = SoftwareReleaseAssignment.objects.all()
    serializer_class = SoftwareReleaseAssignmentSerializer
    filterset_class = SoftwareReleaseAssignmentFilterSet

class DeviceTypeFamilyViewSet(NetBoxModelViewSet):
    queryset = DeviceTypeFamily.objects.prefetch_related('device_types')
    serializer_class = DeviceTypeFamilySerializer
    filterset_class = DeviceTypeFamilyFilterSet

class SoftwareReleaseCompatibilityViewSet(NetBoxModelViewSet):
    queryset = SoftwareReleaseCompatibility.objects.all()
    serializer_class = SoftwareReleaseCompatibilitySerializer
    filterset_class = SoftwareReleaseCompatibilityFilterSet