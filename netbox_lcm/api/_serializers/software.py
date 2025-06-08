from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import DeviceSerializer, DeviceTypeSerializer, DeviceRoleSerializer
from dcim.models import Device, DeviceType, DeviceRole, Manufacturer
from netbox_lcm.models import DeviceTypeFamily, SoftwareProduct, SoftwareRelease, SoftwareReleaseStatus, SoftwareReleaseAssignment


__all__ = (
    'DeviceTypeFamilySerializer',
    'SoftwareProductSerializer',
    'SoftwareReleaseSerializer',
    'SoftwareReleaseStatusSerializer',
    'SoftwareReleaseAssignmentSerializer',
)

class DeviceTypeFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lcm-api:devicetypefamily-detail'
    )
    manufacturer = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all()
    )
    device_types = serializers.PrimaryKeyRelatedField(
        queryset=DeviceType.objects.all(),
        many=True
    )
    class Meta:
        model = DeviceTypeFamily
        fields = [
            'id', 'url', 'display',
            'name', 'manufacturer',
            'device_types', 'description',
            'created', 'last_updated'
        ]

class SoftwareProductSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_lcm-api:softwareproduct-detail'
    )
    class Meta:
        model = SoftwareProduct
        fields = [
            'id', 'url', 'display', 'name', 'platform',
            'major_version', 'minor_version', 'alias',
            'release_date', 'end_of_security_date', 'end_of_support_date',
            'documentation_url', 'created', 'last_updated',
        ]

class SoftwareReleaseSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:softwarerelease-detail')
    product = serializers.PrimaryKeyRelatedField(queryset=SoftwareProduct.objects.all())
    devicetype_family = DeviceTypeFamilySerializer(read_only=True)
    devicetype_family_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceTypeFamily.objects.all(),
        source='devicetype_family',
        write_only=True
    )
    device_role = serializers.PrimaryKeyRelatedField(queryset=DeviceRole.objects.all(), allow_null=True)

    class Meta:
        model = SoftwareRelease
        fields = [
            'id', 'url', 'display', 'product', 'version',
            'devicetype_family', 'devicetype_family_id',
            'device_role', 'status',
            'created', 'last_updated',
        ]
class SoftwareReleaseStatusSerializer(NetBoxModelSerializer):
    release = serializers.PrimaryKeyRelatedField(queryset=SoftwareRelease.objects.all())
    device_role = serializers.PrimaryKeyRelatedField(queryset=DeviceRole.objects.all(), allow_null=True)

    class Meta:
        model = SoftwareReleaseStatus
        fields = [
            'id', 'url', 'display',
            'release', 'device_role', 'status',
            'created', 'last_updated',
        ]

class SoftwareReleaseAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:softwarereleaseassignment-detail')
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    release = serializers.PrimaryKeyRelatedField(queryset=SoftwareRelease.objects.all())

    class Meta:
        model = SoftwareReleaseAssignment
        fields = [
            'id', 'url', 'display', 'device', 'release',
            'assigned', 'currently_active',
            'created', 'last_updated',
        ]