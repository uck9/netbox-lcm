from netbox.api.viewsets import NetBoxModelViewSet
from ..models import DeviceBackupPolicy, DeviceBackupResult
from netbox_lcm.serializers import DeviceBackupPolicySerializer, DeviceBackupResultSerializer
from netbox_lcm.filtersets import DeviceBackupPolicyFilterSet, DeviceBackupResultFilterSet

__all__ = (
    'DeviceBackupPolicyViewSet',
    'DeviceBackupResultViewSet',
)

class DeviceBackupPolicyViewSet(NetBoxModelViewSet):
    queryset = DeviceBackupPolicy.objects.prefetch_related('device')
    serializer_class = DeviceBackupPolicySerializer
    filterset_class = DeviceBackupPolicyFilterSet

class DeviceBackupResultViewSet(NetBoxModelViewSet):
    queryset = DeviceBackupResult.objects.select_related('policy__device')
    serializer_class = DeviceBackupResultSerializer
    filterset_class = DeviceBackupResultFilterSet