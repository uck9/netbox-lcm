# netbox_lcm/tables.py
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from django.contrib.contenttypes.models import ContentType
from netbox_lcm.models import ExternalAssessment

__all__ = (
    'ExternalAssessmentTable',
)

class ExternalAssessmentTable(NetBoxTable):
    pk = columns.ToggleColumn()
    assessment_type = tables.Column(linkify=True)
    status = tables.Column()
    score = tables.Column()
    observed_at = tables.DateTimeColumn()
    source = tables.Column()
    is_latest = columns.BooleanColumn()
    target = tables.Column(accessor="target_id", verbose_name="Target")
    external_url = tables.LinkColumn(text="Report", accessor="external_url", verbose_name="Report", orderable=False)

    class Meta(NetBoxTable.Meta):
        model = ExternalAssessment
        fields = (
            "pk", "assessment_type", "status", "score", "observed_at",
            "source", "is_latest", "target", "external_url",
        )
        default_columns = (
            "assessment_type", "status", "score", "observed_at",
            "source", "is_latest", "target",
        )

    def render_target(self, record):
        # Lightweight target display without requiring NB linkification helpers
        ct: ContentType = record.target_type
        return f"{ct.app_label}.{ct.model}:{record.target_id}"
