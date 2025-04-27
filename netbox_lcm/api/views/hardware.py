from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lcm.api.serializers import HardwareLifecycleSerializer
from netbox_lcm.filtersets import HardwareLifecycleFilterSet
from netbox_lcm.models import HardwareLifecycle


__all__ = (
    'HardwareLifecycleViewSet',
)


class HardwareLifecycleViewSet(NetBoxModelViewSet):
    queryset = HardwareLifecycle.objects.all()
    serializer_class = HardwareLifecycleSerializer
    filterset_class = HardwareLifecycleFilterSet
