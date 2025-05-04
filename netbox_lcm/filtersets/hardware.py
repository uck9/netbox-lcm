import django_filters
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.db.models import Q

from dcim.models import ModuleType, DeviceType, Device
from netbox.filtersets import NetBoxModelFilterSet
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan


__all__ = (
    'HardwareLifecycleFilterSet',
    'HardwareLifecyclePlanFilterSet',
)


class HardwareLifecycleFilterSet(NetBoxModelFilterSet):
    assigned_object_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.all()
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__model',
        queryset=DeviceType.objects.all(),
        to_field_name='model',
        label=_('Device Type (Model)'),
        method='filter_types',
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label=_('Device Type'),
        method='filter_types',
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='model',
        label=_('Module Type (Model)'),
        method='filter_types',
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type',
        queryset=ModuleType.objects.all(),
        label=_('Module Type'),
        method='filter_types',
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'id', 'assigned_object_type_id', 'assigned_object_id', 'end_of_sale', 'end_of_maintenance', 'end_of_security', 'last_contract_attach', 'last_contract_renewal', 'end_of_support',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(
            Q(device_type__model__icontains=value) |
            Q(module_type__model__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_types(self, queryset, name, value):
        if '__' in name:
            name, leftover = name.split('__', 1)

        if type(value) is list:
            name = f'{name}__in'

        if not value:
            return queryset
        try:
            return queryset.filter(**{f'{name}': value})
        except ValueError:
            return queryset.none()


class HardwareLifecyclePlanFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label=_('Device'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label=_('Device'),
    )

    class Meta:
        model = HardwareLifecyclePlan
        fields = (
            'id', 'device', 'plan_type', 'status', 'resourcing_type', 'completion_by', 'is_supported',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
