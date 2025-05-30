from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan
from utilities.api import get_serializer_for_model


__all__ = (
    'HardwareLifecycleSerializer',
    'HardwareLifecyclePlanSerializer',
)


class HardwareLifecycleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:hardwarelifecycle-detail')
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )

    end_of_sale = serializers.DateField()
    end_of_maintenance = serializers.DateField(required=False)
    end_of_security = serializers.DateField(required=False)
    last_contract_attach = serializers.DateField(required=False)
    last_contract_renewal = serializers.DateField(required=False)
    end_of_support = serializers.DateField()
    notice_url = serializers.URLField(required=False)

    class Meta:
        model = HardwareLifecycle
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object_count', 'end_of_sale',
            'end_of_maintenance', 'end_of_security', 'last_contract_attach', 'last_contract_renewal', 'end_of_support',
            'notice_url', 'migration_pid', 'migration_pid_cost', 'migration_pid_cost_currency', 'migration_calc_key',
            'calc_replacement_year', 'calc_budget_year', 'description', 'comments', 'custom_fields',
        )
        brief_fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'end_of_sale', 'assigned_object_count',
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, instance):
        serializer = get_serializer_for_model(instance.assigned_object)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, context=context, nested=True).data


class HardwareLifecyclePlanSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:hardwarelifecycleplan-detail')
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    completion_by = serializers.DateField()

    class Meta:
        model = HardwareLifecyclePlan
        fields = (
            'url', 'id', 'display', 'device', 'plan_type', 'status', 'resourcing_type', 'completion_by',
            'description', 'comments', 'custom_fields',
        )
        brief_fields = (
            'url', 'id', 'display', 'device', 'plan_type', 'status', 'resourcing_type', 'completion_by',
        )
