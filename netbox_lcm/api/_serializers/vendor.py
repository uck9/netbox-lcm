from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.models import Vendor

__all__ = (
    'VendorSerializer',
)


class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_lcm-api:vendor-detail')

    class Meta:
        model = Vendor
        fields = ('url', 'id', 'display', 'name', 'description', 'comments', 'custom_fields', )
        brief_fields = ('url', 'id', 'display', 'name', )
