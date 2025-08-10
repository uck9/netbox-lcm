# netbox_lcm/api/serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ..models.external import ExternalAssessment, ExternalAssessmentType


__all__ = (
    'ContentTypeField',
    'ExternalAssessmentTypeSerializer',
    'ExternalAssessmentSerializer',
)


class ContentTypeField(serializers.SlugRelatedField):
    """
    Accept/return ContentType as 'app_label.model' slug.
    """
    def __init__(self, **kwargs):
        super().__init__(slug_field="model", queryset=ContentType.objects.none(), **kwargs)

    def to_representation(self, obj: ContentType):
        return f"{obj.app_label}.{obj.model}"

    def to_internal_value(self, data):
        try:
            app, model = str(data).split(".", 1)
        except Exception:
            raise serializers.ValidationError("target_type must be 'app_label.model'")
        try:
            return ContentType.objects.get(app_label=app, model=model)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(f"Unknown ContentType: {data}")


class ExternalAssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalAssessmentType
        fields = ["slug", "label", "default_retention_days", "higher_is_better", "ui_badge"]


class ExternalAssessmentSerializer(serializers.ModelSerializer):
    target_type = ContentTypeField()
    class Meta:
        model = ExternalAssessment
        read_only_fields = ["id", "created", "updated", "is_latest"]
        fields = [
            "id", "assessment_type", "target_type", "target_id",
            "source", "source_run_id", "external_reference",
            "observed_at", "expires_at", "retention_days",
            "status", "score", "summary", "details", "external_url",
            "is_latest", "created", "updated",
        ]
