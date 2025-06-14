from netbox.api.viewsets import NetBoxModelViewSet
from netbox_lcm.api.serializers import DeviceLifecycleSerializer
from netbox_lcm.filtersets import DeviceLifecycleFilterSet
from netbox_lcm.models import HardwareLifecycle, SupportContractAssignment
from dcim.models import Device

from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery, Prefetch

__all__ = (
    'DeviceLifecycleViewSet',
)


class DeviceLifecycleViewSet(NetBoxModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceLifecycleSerializer
    filterset_class = DeviceLifecycleFilterSet
    
    def get_queryset(self):
        device_type_ct = ContentType.objects.get_for_model(Device._meta.get_field('device_type').related_model)

        # Base queryset
        qs = Device.objects.annotate(
            hw_end_of_sale=Subquery(
                HardwareLifecycle.objects.filter(
                    assigned_object_type=device_type_ct,
                    assigned_object_id=OuterRef('device_type_id')
                ).values('end_of_sale')[:1]
            ),
            hw_end_of_support=Subquery(
                HardwareLifecycle.objects.filter(
                    assigned_object_type=device_type_ct,
                    assigned_object_id=OuterRef('device_type_id')
                ).values('end_of_support')[:1]
            ),
            hw_end_of_security=Subquery(
                HardwareLifecycle.objects.filter(
                    assigned_object_type=device_type_ct,
                    assigned_object_id=OuterRef('device_type_id')
                ).values('end_of_security')[:1]
            ),
        ).select_related(
            'device_type__manufacturer', 'site'
        ).prefetch_related(
            Prefetch(
                'contracts',
                queryset=SupportContractAssignment.objects.select_related('contract', 'sku'),
                to_attr='prefetched_contracts'
            )
        ).exclude(
            status__in=['unmanaged', 'passive']
        )

        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Preload all lifecycle records for relevant device types
        device_type_ids = self.get_queryset().values_list('device_type_id', flat=True).distinct()
        device_type_ct = ContentType.objects.get_for_model(Device._meta.get_field('device_type').related_model)

        lifecycles = HardwareLifecycle.objects.filter(
            assigned_object_type=device_type_ct,
            assigned_object_id__in=device_type_ids
        )

        context['lifecycle_map'] = {
            (device_type_ct.id, lc.assigned_object_id): lc
            for lc in lifecycles
        }
        context['device_type_ct_id'] = device_type_ct.id
        return context
