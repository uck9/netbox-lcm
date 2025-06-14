import django_filters
from django.utils.translation import gettext as _
from django.db.models import Q

from dcim.choices import DeviceStatusChoices
from dcim.models import Device, Site, DeviceType, Manufacturer
from tenancy.models import Tenant, TenantGroup
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models import SupportContractAssignment, HardwareLifecycle

__all__ = (
    'DeviceLifecycleFilterSet',
)


class DeviceLifecycleFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Device Name"
    )
    site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label='Site'
    )
    tenant_group = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__group',
        queryset=TenantGroup.objects.all()
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all()
    )
    status = django_filters.MultipleChoiceFilter(
        choices=DeviceStatusChoices,
        null_value=None
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        field_name='device_type__manufacturer',
        label="Manufacturer"
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        label="Device Type"
    )
    has_primary_ip = django_filters.BooleanFilter(
        method='filter_has_primary_ip',
        label='Has Primary IP'
    )
    has_support_contract = django_filters.BooleanFilter(
        method='filter_has_contract',
        label="Has Support Contract"
    )
    support_contract_end_before = django_filters.DateFilter(
        method='filter_contract_end_before',
        label="Contract ends before"
    )
    hw_eosec_before = django_filters.DateFilter(
        field_name='hw_end_of_security',
        lookup_expr='lte',
        label="HW End of Security before"
    )

    class Meta:
        model = Device
        fields = [
            'name', 'site', 'tenant_group', 'tenant', 'manufacturer', 'device_type', 
            'has_primary_ip', 'has_support_contract', 'support_contract_end_before', 
            'hw_eosec_before'
        ]

    def filter_has_primary_ip(self, queryset, name, value):
        if value:
            return queryset.exclude(primary_ip4__isnull=True, primary_ip6__isnull=True)
        else:
            return queryset.filter(primary_ip4__isnull=True, primary_ip6__isnull=True)

    def filter_has_contract(self, queryset, name, value):
        if value:
            return queryset.filter(contracts__isnull=False).distinct()
        else:
            return queryset.filter(contracts__isnull=True).distinct()

    def filter_contract_end_before(self, queryset, name, value):
        return queryset.filter(contracts__end__lte=value).distinct()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
        