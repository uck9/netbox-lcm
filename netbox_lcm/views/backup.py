from netbox.views.generic import ( ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, ObjectChildrenView,
    BulkDeleteView, BulkEditView )
from netbox_lcm.models import DeviceBackupPolicy, DeviceBackupResult
from netbox_lcm.forms import (
    DeviceBackupPolicyForm, DeviceBackupPolicyFilterForm, DeviceBackupPolicyBulkEditForm,
    DeviceBackupResultForm, DeviceBackupResultFilterForm, DeviceBackupResultBulkEditForm
)
from netbox_lcm.tables import DeviceBackupPolicyTable, DeviceBackupResultTable

__all__ = (
    # DeviceBackupPolicy
    'DeviceBackupPolicyListView',
    'DeviceBackupPolicyView',
    'DeviceBackupPolicyEditView',
    'DeviceBackupPolicyDeleteView',
    'DeviceBackupPolicyBulkEditView',
    'DeviceBackupPolicyBulkDeleteView',

    # DeviceBackupResult
    'DeviceBackupResultListView',
    'DeviceBackupResultView',
    'DeviceBackupResultEditView',
    'DeviceBackupResultDeleteView',
    'DeviceBackupResultBulkEditView',
    'DeviceBackupResultBulkDeleteView',
)

# Device Backup Policy Views
class DeviceBackupPolicyListView(ObjectListView):
    queryset = DeviceBackupPolicy.objects.prefetch_related('device')
    table = DeviceBackupPolicyTable
    filterset_form = DeviceBackupPolicyFilterForm

class DeviceBackupPolicyView(ObjectView):
    queryset = DeviceBackupPolicy.objects.prefetch_related('device', 'results')

class DeviceBackupPolicyEditView(ObjectEditView):
    queryset = DeviceBackupPolicy.objects.all()
    form = DeviceBackupPolicyForm

class DeviceBackupPolicyDeleteView(ObjectDeleteView):
    queryset = DeviceBackupPolicy.objects.all()

class DeviceBackupPolicyBulkEditView(BulkEditView):
    queryset = DeviceBackupPolicy.objects.all()
    table = DeviceBackupPolicyTable
    form = DeviceBackupPolicyBulkEditForm

class DeviceBackupPolicyBulkDeleteView(BulkDeleteView):
    queryset = DeviceBackupPolicy.objects.all()
    table = DeviceBackupPolicyTable

# Device Backup Result Views
class DeviceBackupResultListView(ObjectListView):
    queryset = DeviceBackupResult.objects.select_related('policy', 'policy__device')
    table = DeviceBackupResultTable
    filterset_form = DeviceBackupResultFilterForm

class DeviceBackupResultView(ObjectView):
    queryset = DeviceBackupResult.objects.select_related('policy', 'policy__device')

class DeviceBackupResultEditView(ObjectEditView):
    queryset = DeviceBackupResult.objects.all()
    form = DeviceBackupResultForm

class DeviceBackupResultDeleteView(ObjectDeleteView):
    queryset = DeviceBackupResult.objects.all()

class DeviceBackupResultBulkEditView(BulkEditView):
    queryset = DeviceBackupResult.objects.all()
    table = DeviceBackupResultTable
    form = DeviceBackupResultBulkEditForm

class DeviceBackupResultBulkDeleteView(BulkDeleteView):
    queryset = DeviceBackupResult.objects.all()
    table = DeviceBackupResultTable
