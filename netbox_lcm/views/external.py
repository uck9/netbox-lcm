# netbox_lcm/views.py
from netbox.views import generic
from .models.external import ExternalAssessment
from .filters import ExternalAssessmentFilter
from .tables import ExternalAssessmentTable
from .forms import ExternalAssessmentFilterForm

__all__ = (
    'ExternalAssessmentListView',
)


class ExternalAssessmentListView(generic.ObjectListView):
    """
    Read-only list. We’re not using NetBoxModel, but ObjectListView still works with a queryset + table.
    """
    queryset = ExternalAssessment.objects.all()
    table = ExternalAssessmentTable
    filterset = ExternalAssessmentFilter
    filterset_form = ExternalAssessmentFilterForm
    action_buttons = ()  # no add/edit
