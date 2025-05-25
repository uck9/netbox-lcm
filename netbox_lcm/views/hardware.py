from netbox.views.generic import (ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, BulkEditView,
                                  BulkDeleteView)
from netbox_lcm.filtersets import HardwareLifecycleFilterSet, HardwareLifecyclePlanFilterSet
from netbox_lcm.forms import HardwareLifecycleFilterForm, HardwareLifecycleBulkEditForm, \
    HardwareLifecyclePlanFilterForm, HardwareLifecyclePlanBulkEditForm
from netbox_lcm.forms.model_forms import HardwareLifecycleForm, HardwareLifecyclePlanForm
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan
from netbox_lcm.tables import HardwareLifecycleTable, HardwareLifecyclePlanTable
from utilities.views import register_model_view


__all__ = (
    'HardwareLifecycleListView',
    'HardwareLifecycleView',
    'HardwareLifecycleEditView',
    'HardwareLifecycleBulkEditView',
    'HardwareLifecycleDeleteView',
    'HardwareLifecycleBulkDeleteView',
    'HardwareLifecyclePlanListView',
    'HardwareLifecyclePlanView',
    'HardwareLifecyclePlanEditView',
    'HardwareLifecyclePlanBulkEditView',
    'HardwareLifecyclePlanDeleteView',
    'HardwareLifecyclePlanBulkDeleteView',
)


@register_model_view(HardwareLifecycle, name='list')
class HardwareLifecycleListView(ObjectListView):
    queryset = HardwareLifecycle.objects.all()
    table = HardwareLifecycleTable
    filterset = HardwareLifecycleFilterSet
    filterset_form = HardwareLifecycleFilterForm


@register_model_view(HardwareLifecycle)
class HardwareLifecycleView(ObjectView):
    queryset = HardwareLifecycle.objects.all()

    def get_extra_context(self, request, instance):

        return {
        }


@register_model_view(HardwareLifecycle, 'edit')
class HardwareLifecycleEditView(ObjectEditView):
    template_name = 'netbox_lcm/hardwarelifecycle_edit.html'
    queryset = HardwareLifecycle.objects.all()
    form = HardwareLifecycleForm


@register_model_view(HardwareLifecycle, 'bulk_edit')
class HardwareLifecycleBulkEditView(BulkEditView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable
    form = HardwareLifecycleBulkEditForm


@register_model_view(HardwareLifecycle, 'delete')
class HardwareLifecycleDeleteView(ObjectDeleteView):
    queryset = HardwareLifecycle.objects.all()


@register_model_view(HardwareLifecycle, 'bulk_delete')
class HardwareLifecycleBulkDeleteView(BulkDeleteView):
    queryset = HardwareLifecycle.objects.all()
    filterset = HardwareLifecycleFilterSet
    table = HardwareLifecycleTable


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
