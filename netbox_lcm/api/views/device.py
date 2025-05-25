from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lcm.api.serializers import DeviceLifecycleSerializer
from netbox_lcm.filtersets import DeviceLifecycleFilterSet
from dcim.models import Device

__all__ = (
    'DeviceLifecycleViewSet',
)


class DeviceLifecycleViewSet(NetBoxModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceLifecycleSerializer
    filterset_class = DeviceLifecycleFilterSet
