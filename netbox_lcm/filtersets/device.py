import django_filters
from django.utils.translation import gettext as _

from dcim.models import Device, Site, DeviceType
from dcim.choices import DeviceStatusChoices
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
    device_type = django_filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        label="Device Type"
    )
    site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label='Site'
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
            'name', 'device_type', 'site', 
            'has_support_contract', 'support_contract_end_before', 'hw_eosec_before']

    def filter_has_contract(self, queryset, name, value):
        if value:
            return queryset.filter(contracts__isnull=False).distinct()
        else:
            return queryset.filter(contracts__isnull=True).distinct()

    def filter_contract_end_before(self, queryset, name, value):
        return queryset.filter(contracts__end__lte=value).distinct()
        