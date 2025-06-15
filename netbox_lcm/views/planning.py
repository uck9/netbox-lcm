from netbox.views.generic import (ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, BulkEditView,
                                  BulkDeleteView)
from netbox_lcm.filtersets import HardwareLifecycleFilterSet, HardwareLifecyclePlanFilterSet
from netbox_lcm.forms import HardwareLifecyclePlanFilterForm, HardwareLifecyclePlanBulkEditForm
from netbox_lcm.forms.model_forms import HardwareLifecyclePlanForm
from netbox_lcm.models import HardwareLifecyclePlan
from netbox_lcm.tables import HardwareLifecycleTable, HardwareLifecyclePlanTable
from utilities.views import register_model_view


__all__ = (
    'HardwareLifecyclePlanListView',
    'HardwareLifecyclePlanView',
    'HardwareLifecyclePlanEditView',
    'HardwareLifecyclePlanBulkEditView',
    'HardwareLifecyclePlanDeleteView',
    'HardwareLifecyclePlanBulkDeleteView',
)


# Hardware Lifecycle Plans
@register_model_view(HardwareLifecyclePlan, name='list')
class HardwareLifecyclePlanListView(ObjectListView):
    queryset = HardwareLifecyclePlan.objects.all()
    table = HardwareLifecyclePlanTable
    filterset = HardwareLifecyclePlanFilterSet
    filterset_form = HardwareLifecyclePlanFilterForm


@register_model_view(HardwareLifecyclePlan)
class HardwareLifecyclePlanView(ObjectView):
    queryset = HardwareLifecyclePlan.objects.all()


@register_model_view(HardwareLifecyclePlan, 'edit')
class HardwareLifecyclePlanEditView(ObjectEditView):
    template_name = 'netbox_lcm/hardwarelifecycleplan_edit.html'
    queryset = HardwareLifecyclePlan.objects.all()
    form = HardwareLifecyclePlanForm


@register_model_view(HardwareLifecyclePlan, 'bulk_edit')
class HardwareLifecyclePlanBulkEditView(BulkEditView):
    queryset = HardwareLifecyclePlan.objects.all()
    filterset = HardwareLifecyclePlanFilterSet
    table = HardwareLifecyclePlanTable
    form = HardwareLifecyclePlanBulkEditForm


@register_model_view(HardwareLifecyclePlan, 'delete')
class HardwareLifecyclePlanDeleteView(ObjectDeleteView):
    queryset = HardwareLifecyclePlan.objects.all()


@register_model_view(HardwareLifecyclePlan, 'bulk_delete')
class HardwareLifecyclePlanBulkDeleteView(BulkDeleteView):
    queryset = HardwareLifecyclePlan.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable
