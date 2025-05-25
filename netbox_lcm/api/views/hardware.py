from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lcm.api.serializers import HardwareLifecycleSerializer, HardwareLifecyclePlanSerializer
from netbox_lcm.filtersets import HardwareLifecycleFilterSet, HardwareLifecyclePlanFilterSet
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan

__all__ = (
    'HardwareLifecycleViewSet',
    'HardwareLifecyclePlanViewSet',
)


class HardwareLifecycleViewSet(NetBoxModelViewSet):
    queryset = HardwareLifecycle.objects.all()
    serializer_class = HardwareLifecycleSerializer
    filterset_class = HardwareLifecycleFilterSet


class HardwareLifecyclePlanViewSet(NetBoxModelViewSet):
    queryset = HardwareLifecyclePlan.objects.all()
    serializer_class = HardwareLifecyclePlanSerializer
    filterset_class = HardwareLifecyclePlanFilterSet
