from rest_framework import serializers
from dcim.api.serializers_.devices import DeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_lcm.models import DeviceBackupPolicy, DeviceBackupResult

__all__ = (
    'DeviceBackupPolicySerializer',
    'DeviceBackupResultSerializer',
)


class DeviceBackupPolicySerializer(NetBoxModelSerializer):
    device = DeviceSerializer(nested=True, required=False, allow_null=True)
    backup_health_score = serializers.SerializerMethodField()
    backup_health_label = serializers.SerializerMethodField()

    class Meta:
        model = DeviceBackupPolicy
        fields = [
            'id', 'url', 'display', 'device', 'enabled', 'evaluate_status',
            'backup_system', 'destination', 'method', 'notes',
            'backup_health_score', 'backup_health_label',
            'created', 'last_updated'
        ]

    def get_backup_health_score(self, obj):
        return obj.get_backup_health_score()

    def get_backup_health_label(self, obj):
        return obj.backup_health_label

    def get_days_since_last_success(self, obj):
        return obj.days_since_last_success


class DeviceBackupResultSerializer(NetBoxModelSerializer):
    policy = serializers.PrimaryKeyRelatedField(queryset=DeviceBackupPolicy.objects.all())
    device = DeviceSerializer(source='policy.device', nested=True, read_only=True)

    class Meta:
        model = DeviceBackupResult
        fields = [
            'id', 'url', 'display', 'policy', 'device',
            'backup_date', 'status', 'details',
            'created', 'last_updated'
        ]
