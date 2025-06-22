from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from dcim.api.serializers_.manufacturers import ManufacturerSerializer
from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.api._serializers.license import LicenseAssignmentSerializer
from netbox_lcm.api._serializers.vendor import VendorSerializer
from netbox_lcm.choices.contract import SupportCoverageStatusChoices
from netbox_lcm.models import Vendor, SupportContract, SupportContractAssignment, SupportSKU
from netbox.api.fields import ChoiceField

__all__ = (
    'SupportSKUSerializer',
    'SupportContractSerializer',
    'SupportContractAssignmentSerializer',
)


class SupportSKUSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:supportsku-detail')
    manufacturer = ManufacturerSerializer(nested=True)

    class Meta:
        model = SupportSKU
        fields = ('url', 'id', 'display', 'manufacturer', 'sku', 'description', 'comments', 'custom_fields' )
        brief_fields = ('url', 'id', 'display', 'manufacturer', 'sku', )


class SupportContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:supportcontract-detail')
    vendor = VendorSerializer(nested=True)
    start = serializers.DateField(required=False)
    renewal = serializers.DateField(required=False)
    end = serializers.DateField(required=False)

    class Meta:
        model = SupportContract
        fields = (
            'url', 'id', 'display', 'vendor', 'contract_id', 'start', 'renewal', 'end', 'description', 'comments', 'custom_fields',
        )
        brief_fields = ('url', 'id', 'display', 'vendor', 'contract_id', )


class SupportContractAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:supportcontractassignment-detail')
    contract = SupportContractSerializer(nested=True)
    sku = SupportSKUSerializer(nested=True, required=False, allow_null=True)
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    support_coverage_status = ChoiceField(choices=SupportCoverageStatusChoices)
    license = LicenseAssignmentSerializer(nested=True, required=False, allow_null=True)
    start = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        model = SupportContractAssignment
        fields = (
            'url', 'id', 'display', 'contract', 'sku', 'device', 'license', 'start', 'end_date', 
            'support_coverage_status', 'tags', 'description', 'comments', 'custom_fields',
        )

        brief_fields = ('url', 'id', 'display', 'contract', 'sku', 'device', 'license', 'start', 'end_date', 'support_coverage_status')
