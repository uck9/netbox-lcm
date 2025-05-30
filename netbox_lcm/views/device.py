from django.db.models import OuterRef, Subquery, Value, Prefetch
from netbox.views.generic import ObjectListView
from django.contrib.contenttypes.models import ContentType
from dcim.models import Device, DeviceType
from netbox_lcm.filtersets import DeviceLifecycleFilterSet
from netbox_lcm.forms.filtersets import DeviceLifecycleFilterForm
from netbox_lcm.models import HardwareLifecycle, SupportContractAssignment, SupportContract
from netbox_lcm.tables import DeviceLifecycleTable

__all__ = (
    'DeviceLifecycleListView',
)

class DeviceLifecycleListView(ObjectListView):
    queryset = Device.objects.all()
    table = DeviceLifecycleTable
    filterset = DeviceLifecycleFilterSet
    filterset_form = DeviceLifecycleFilterForm
    template_name = 'netbox_lcm/devicelifecycle.html'
    actions = {
        'export': {'view'},
    }

    def get_queryset(self, request):

        # ContentType for DeviceType
        device_type_ct = ContentType.objects.get_for_model(Device._meta.get_field('device_type').related_model)

        # Subqueries for lifecycle fields
        lifecycle_qs = HardwareLifecycle.objects.filter(
            assigned_object_type=device_type_ct,
            assigned_object_id=OuterRef('device_type_id')
        )

        qs = super().get_queryset(request).annotate(
            hw_end_of_sale=Subquery(lifecycle_qs.values('end_of_sale')[:1]),
            hw_end_of_support=Subquery(lifecycle_qs.values('end_of_support')[:1]),
            hw_end_of_security=Subquery(lifecycle_qs.values('end_of_security')[:1])
        ).select_related(
            'device_type__manufacturer'
        ).prefetch_related(
            Prefetch(
                'contracts',
                queryset=SupportContractAssignment.objects.select_related('contract', 'sku'),
                to_attr='prefetched_contracts'
            )
        )

        qs = qs.exclude(status='unmanaged')
        qs = qs.exclude(status='passive')

        return qs
