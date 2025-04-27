from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lcm.api.serializers import LicenseSerializer, LicenseAssignmentSerializer
from netbox_lcm.filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from netbox_lcm.models import License, LicenseAssignment


__all__ = (
    'LicenseViewSet',
    'LicenseAssignmentViewSet'
)


class LicenseViewSet(NetBoxModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilterSet


class LicenseAssignmentViewSet(NetBoxModelViewSet):
    queryset = LicenseAssignment.objects.all()
    serializer_class = LicenseAssignmentSerializer
    filterset_class = LicenseAssignmentFilterSet
