# netbox_lcm/views.py
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView, \
    BulkDeleteView, BulkEditView
from netbox_lcm.forms import ExternalAssessmentForm
from netbox.views import generic
from netbox_lcm.models import ExternalAssessment
from netbox_lcm.filtersets import ExternalAssessmentFilter
from netbox_lcm.tables import ExternalAssessmentTable
from netbox_lcm.forms import ExternalAssessmentFilterForm

from utilities.views import ViewTab, register_model_view, GetRelatedModelsMixin

__all__ = (
    'ExternalAssessmentListView',
    'ExternalAssessmentView',
    'ExternalAssessmentEditView',
    'ExternalAssessmentDeleteView',
)

@register_model_view(ExternalAssessment, name='list')
class ExternalAssessmentListView(ObjectListView):
    queryset = ExternalAssessment.objects.all()
    table = ExternalAssessmentTable
    filterset = ExternalAssessmentFilter
    filterset_form = ExternalAssessmentFilterForm
    actions = {
        'export': {'view'},
    }


@register_model_view(ExternalAssessment)
class ExternalAssessmentView(ObjectView):
    queryset = ExternalAssessment.objects.all()
    actions = {}


class ExternalAssessmentEditView(ObjectEditView):
    queryset = ExternalAssessment.objects.all()
    form = ExternalAssessmentForm


class ExternalAssessmentDeleteView(ObjectDeleteView):
    queryset = ExternalAssessment.objects.all()