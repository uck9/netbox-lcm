from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from dcim.api.serializers_.devicetypes import DeviceTypeSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan
from netbox_lcm.api._serializers.contract import SupportSKUSerializer
from utilities.api import get_serializer_for_model

from dcim.api.nested import (
    NestedDeviceSerializer,
    NestedDeviceTypeSerializer,
    NestedSiteSerializer,
)

__all__ = (
    'HardwareLifecycleSerializer',
)

# -device
# site
# status
# hw_end_of_security
# device_type
# contract_id
#- contract_sku
# contract_end

class DeviceLifecycleSerializer(serializers.Serializer):
    device = NestedDeviceSerializer()
    device_type = NestedDeviceTypeSerializer()
    site = NestedSiteSerializer()
    status = serializers.CharField(allow_null=True)
    support_contract_id = serializers.CharField(allow_null=True)
    support_contract_end = serializers.DateField(allow_null=True)
    hw_end_of_security = serializers.DateField(allow_null=True)