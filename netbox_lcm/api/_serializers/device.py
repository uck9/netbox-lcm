from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from dcim.api.serializers_.devicetypes import DeviceTypeSerializer
from dcim.api.serializers_.sites import SiteSerializer
from dcim.models import Device
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.choices import SupportCoverageStatusChoices
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan, SupportContractAssignment
from netbox_lcm.api._serializers.contract import SupportContractAssignmentSerializer
from utilities.api import get_serializer_for_model

__all__ = (
    'HardwareLifecycleDetailsSerializer',
    'DeviceLifecycleSerializer',
)


class HardwareLifecycleDetailsSerializer(serializers.Serializer):
    is_supported = serializers.SerializerMethodField()
    days_to_vendor_eos = serializers.SerializerMethodField()
    calc_budget_year = serializers.SerializerMethodField()
    calc_replacement_year = serializers.SerializerMethodField()
    hw_end_of_sale = serializers.DateField(read_only=True)
    hw_end_of_security = serializers.DateField(read_only=True)
    hw_end_of_support = serializers.DateField(read_only=True)

    def get_lifecycle(self, obj):
        return self.context.get('lifecycle')

    def get_calc_budget_year(self, obj):
        lifecycle = self.get_lifecycle(obj)
        return lifecycle.calc_budget_year if lifecycle else None
    
    def get_calc_replacement_year(self, obj):
        lifecycle = self.get_lifecycle(obj)
        return lifecycle.calc_replacement_year if lifecycle else None
    
    def get_is_supported(self, obj):
        lifecycle = self.get_lifecycle(obj)
        return lifecycle.is_supported if lifecycle else None

    def get_days_to_vendor_eos(self, obj):
        lifecycle = self.get_lifecycle(obj)
        return lifecycle.days_to_vendor_eos if lifecycle else None


class DeviceLifecycleSerializer(NetBoxModelSerializer):
    device_type = DeviceTypeSerializer(nested=True)
    site = SiteSerializer(nested=True)
    status = serializers.CharField(allow_null=True)
    support_coverage_status = serializers.SerializerMethodField()
    support_contract_count = serializers.IntegerField(read_only=True)
    support_contracts = SupportContractAssignmentSerializer(
        nested=True, source='prefetched_contracts', many=True, read_only=True
    )
    hw_lifecycle = serializers.SerializerMethodField()
    

    def get_hw_lifecycle(self, obj):
        lifecycle_map = self.context.get('lifecycle_map', {})
        device_type_ct_id = self.context.get('device_type_ct_id')
        key = (device_type_ct_id, obj.device_type.id)
        lifecycle = lifecycle_map.get(key)

        # Serialize using nested serializer
        context = {'lifecycle': lifecycle}
        serializer = HardwareLifecycleDetailsSerializer(
            obj,
            context=context
        )
        # Manually inject the annotated fields into the serializer
        serializer.fields['hw_end_of_sale'] = serializers.DateField(read_only=True, default=getattr(obj, 'hw_end_of_sale', None))
        serializer.fields['hw_end_of_support'] = serializers.DateField(read_only=True, default=getattr(obj, 'hw_end_of_support', None))
        serializer.fields['hw_end_of_security'] = serializers.DateField(read_only=True, default=getattr(obj, 'hw_end_of_security', None))
        return serializer.data

    def get_support_coverage_status(self, obj):
        value = getattr(obj, 'support_coverage_status', None)
        label = SupportCoverageStatusChoices.get_label(value)
        return {
            "value": value,
            "label": label
        }

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'status', 'site', 'device_type',
            'hw_lifecycle', 'support_coverage_status', 'support_contract_count', 'support_contracts'
        ]