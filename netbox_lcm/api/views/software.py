from netbox.api.viewsets import NetBoxModelViewSet
from dcim.api.views import DeviceViewSet
from netbox_lcm.models import SoftwareProduct, SoftwareRelease, SoftwareReleaseAssignment
from netbox_lcm.filtersets import (
    SoftwareProductFilterSet,
    SoftwareReleaseFilterSet,
    SoftwareReleaseAssignmentFilterSet,
)
from netbox_lcm.api.serializers import (
    SoftwareProductSerializer,
    SoftwareReleaseSerializer,
    SoftwareReleaseAssignmentSerializer,
)

__all__ = (
    'SoftwareProductViewSet',
    'SoftwareReleaseViewSet',
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

#class DeviceModelViewSet(DeviceViewSet):
#    filterset_class = filtersets.DeviceModelViewSet