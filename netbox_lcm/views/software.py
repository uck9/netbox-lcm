from netbox.views import generic
from netbox_lcm.models import SoftwareProduct, SoftwareRelease, SoftwareReleaseAssignment
from netbox_lcm.forms.model_forms import SoftwareProductForm, SoftwareReleaseForm, SoftwareReleaseAssignmentForm
from netbox_lcm.tables import SoftwareProductTable, SoftwareReleaseTable, SoftwareReleaseAssignmentTable
from netbox_lcm.filtersets import SoftwareProductFilterSet, SoftwareReleaseFilterSet, SoftwareReleaseAssignmentFilterSet
from utilities.views import register_model_view

# SoftwareProduct
@register_model_view(SoftwareProduct, name='list')
class SoftwareProductListView(generic.ObjectListView):
    queryset = SoftwareProduct.objects.all()
    table = SoftwareProductTable
    filterset = SoftwareProductFilterSet

@register_model_view(SoftwareProduct)
class SoftwareProductView(generic.ObjectView):
    queryset = SoftwareProduct.objects.all()

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
