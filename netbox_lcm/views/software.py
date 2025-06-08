from netbox.views import generic
from utilities.views import register_model_view, GetRelatedModelsMixin

from netbox_lcm.models import DeviceTypeFamily, SoftwareProduct, SoftwareRelease, SoftwareReleaseCompatability, \
    SoftwareReleaseAssignment
from netbox_lcm.forms.model_forms import DeviceTypeFamilyForm, SoftwareProductForm, SoftwareReleaseForm, \
    SoftwareReleaseAssignmentForm, SoftwareReleaseCompatabilityForm
from netbox_lcm.tables import DeviceTypeFamilyTable, SoftwareProductTable, SoftwareReleaseTable, \
    SoftwareReleaseAssignmentTable, SoftwareReleaseCompatabilityTable
from netbox_lcm.filtersets import DeviceTypeFamilyFilterSet, SoftwareProductFilterSet, \
    SoftwareReleaseFilterSet, SoftwareReleaseAssignmentFilterSet, SoftwareReleaseCompatabilityFilterSet

# SoftwareProduct
@register_model_view(SoftwareProduct, name='list')
class SoftwareProductListView(generic.ObjectListView):
    queryset = SoftwareProduct.objects.all()
    table = SoftwareProductTable
    filterset = SoftwareProductFilterSet

@register_model_view(SoftwareProduct)
class SoftwareProductView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = SoftwareProduct.objects.all()
    
    def get_extra_context(self, request, instance):
        active_assignments = SoftwareReleaseAssignment.objects.filter(
            release__product=instance,
            currently_active=True
        )
        return {
            'related_models': self.get_related_models(
                request,
                instance,
                extra=[(active_assignments, 'release__product')]
            )
        }
    
@register_model_view(SoftwareProduct, name='edit')
class SoftwareProductEditView(generic.ObjectEditView):
    queryset = SoftwareProduct.objects.all()
    form = SoftwareProductForm

@register_model_view(SoftwareProduct, name='delete')
class SoftwareProductDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareProduct.objects.all()

# SoftwareRelease
@register_model_view(SoftwareRelease, name='list')
class SoftwareReleaseListView(generic.ObjectListView):
    queryset = SoftwareRelease.objects.all()
    table = SoftwareReleaseTable
    filterset = SoftwareReleaseFilterSet

@register_model_view(SoftwareRelease)
class SoftwareReleaseView(generic.ObjectView):
    queryset = SoftwareRelease.objects.all()

@register_model_view(SoftwareRelease, name='edit')
class SoftwareReleaseEditView(generic.ObjectEditView):
    queryset = SoftwareRelease.objects.all()
    form = SoftwareReleaseForm

@register_model_view(SoftwareRelease, name='delete')
class SoftwareReleaseDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareRelease.objects.all()

# SoftwareReleaseAssignment
@register_model_view(SoftwareReleaseAssignment, name='list')
class SoftwareReleaseAssignmentListView(generic.ObjectListView):
    queryset = SoftwareReleaseAssignment.objects.all()
    table = SoftwareReleaseAssignmentTable
    filterset = SoftwareReleaseAssignmentFilterSet

    def get(self, request, *args, **kwargs):
        # If no filter is applied, apply default is_active=True
        if not request.GET:
            request.GET = request.GET.copy()
            request.GET['is_active'] = 'true'
        return super().get(request, *args, **kwargs)

@register_model_view(SoftwareReleaseAssignment)
class SoftwareReleaseAssignmentView(generic.ObjectView):
    queryset = SoftwareReleaseAssignment.objects.all()

@register_model_view(SoftwareReleaseAssignment, name='edit')
class SoftwareReleaseAssignmentEditView(generic.ObjectEditView):
    queryset = SoftwareReleaseAssignment.objects.all()
    form = SoftwareReleaseAssignmentForm

@register_model_view(SoftwareReleaseAssignment, name='delete')
class SoftwareReleaseAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareReleaseAssignment.objects.all()

# DeviceTypeFamily
@register_model_view(DeviceTypeFamily, name='list')
class DeviceTypeFamilyListView(generic.ObjectListView):
    queryset = DeviceTypeFamily.objects.prefetch_related('device_types')
    filterset = DeviceTypeFamilyFilterSet
    table = DeviceTypeFamilyTable

@register_model_view(DeviceTypeFamily)
class DeviceTypeFamilyView(generic.ObjectView):
    queryset = DeviceTypeFamily.objects.all()

@register_model_view(DeviceTypeFamily, name='edit')
class DeviceTypeFamilyEditView(generic.ObjectEditView):
    queryset = DeviceTypeFamily.objects.all()
    form = DeviceTypeFamilyForm

@register_model_view(DeviceTypeFamily, name='delete')
class DeviceTypeFamilyDeleteView(generic.ObjectDeleteView):
    queryset = DeviceTypeFamily.objects.all()


class SoftwareReleaseCompatabilityListView(generic.ObjectListView):
    queryset = SoftwareReleaseCompatability.objects.all()
    table = SoftwareReleaseCompatabilityTable
    filterset = SoftwareReleaseCompatabilityFilterSet

class SoftwareReleaseCompatabilityView(generic.ObjectView):
    queryset = SoftwareReleaseCompatability.objects.all()

class SoftwareReleaseCompatabilityEditView(generic.ObjectEditView):
    queryset = SoftwareReleaseCompatability.objects.all()
    form = SoftwareReleaseCompatabilityForm

class SoftwareReleaseCompatabilityDeleteView(generic.ObjectDeleteView):
    queryset = SoftwareReleaseCompatability.objects.all()