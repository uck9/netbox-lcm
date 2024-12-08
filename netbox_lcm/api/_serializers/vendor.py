from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.models import Vendor

__all__ = (
    'VendorSerializer',
)


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:hardwarelifecycle-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name', 'description', 'comments', )
        brief_fields = ('url', 'id', 'display', 'name', )
