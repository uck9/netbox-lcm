# netbox_lcm/filters.py
import django_filters
from django.contrib.contenttypes.models import ContentType
from netbox_lcm.models.external import ExternalAssessment

__all__ = (
    'ExternalAssessmentFilter',
)

class ExternalAssessmentFilter(django_filters.FilterSet):
    target_type = django_filters.ModelChoiceFilter(
        field_name="target_type",
        queryset=ContentType.objects.all(),
    )
    target_id = django_filters.NumberFilter(field_name="target_id")
    assessment_type = django_filters.CharFilter(field_name="assessment_type", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    is_latest = django_filters.BooleanFilter(field_name="is_latest")
    observed_at__gte = django_filters.IsoDateTimeFilter(field_name="observed_at", lookup_expr="gte")
    observed_at__lte = django_filters.IsoDateTimeFilter(field_name="observed_at", lookup_expr="lte")
    source = django_filters.CharFilter(field_name="source", lookup_expr="iexact")
    source_run_id = django_filters.CharFilter(field_name="source_run_id", lookup_expr="exact")

    class Meta:
        model = ExternalAssessment
        fields = [
            "assessment_type", "status", "target_type", "target_id",
            "is_latest", "source", "source_run_id",
        ]
