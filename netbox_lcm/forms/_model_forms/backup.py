# netbox_lcm/forms.py

from django import forms
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import DynamicModelChoiceField, CSVModelChoiceField
from utilities.forms.widgets import BulkEditNullBooleanSelect, DatePicker
from dcim.models import Device

from netbox_lcm.models import DeviceBackupPolicy, DeviceBackupResult
from netbox_lcm.choices import BackupSystemChoices, BackupStatusChoices


# DeviceBackupPolicy Forms
class DeviceBackupPolicyForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=True)

    class Meta:
        model = DeviceBackupPolicy
        fields = (
            'device',
            'enabled',
            'critical',
            'evaluate_status',
            'backup_system',
            'destination',
            'method',
            'notes',
        )


class DeviceBackupPolicyFilterForm(NetBoxModelFilterSetForm):
    model = DeviceBackupPolicy

    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    enabled = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    critical = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    evaluate_status = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    backup_system = forms.ChoiceField(choices=BackupSystemChoices, required=False)

    class Meta:
        fields = ['device', 'enabled', 'critical', 'evaluate_status', 'backup_system']


class DeviceBackupPolicyBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(queryset=DeviceBackupPolicy.objects.all(), widget=forms.MultipleHiddenInput)
    enabled = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    critical = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    evaluate_status = forms.NullBooleanField(required=False, widget=BulkEditNullBooleanSelect)
    backup_system = forms.ChoiceField(choices=BackupSystemChoices, required=False)
    destination = forms.CharField(required=False)
    method = forms.CharField(required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = DeviceBackupPolicy
        nullable_fields = ['destination', 'method', 'notes']


class DeviceBackupPolicyImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(queryset=Device.objects.all())

    class Meta:
        model = DeviceBackupPolicy
        fields = (
            'device',
            'enabled',
            'critical',
            'evaluate_status',
            'backup_system',
            'destination',
            'method',
            'notes',
        )



# DeviceBackupResult Forms
class DeviceBackupResultForm(NetBoxModelForm):
    policy = DynamicModelChoiceField(queryset=DeviceBackupPolicy.objects.all(), required=True)
    backup_date = forms.DateField(
        label=_('End date'),
        required=False,
        widget=DatePicker(),
    )

    class Meta:
        model = DeviceBackupResult
        fields = (
            'policy',
            'backup_date',
            'status',
            'details',
        )


class DeviceBackupResultFilterForm(NetBoxModelFilterSetForm):
    model = DeviceBackupResult

    policy = DynamicModelChoiceField(queryset=DeviceBackupPolicy.objects.all(), required=False)
    status = forms.ChoiceField(choices=BackupStatusChoices, required=False)

    class Meta:
        fields = ['policy', 'status']


class DeviceBackupResultBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(queryset=DeviceBackupResult.objects.all(), widget=forms.MultipleHiddenInput)
    status = forms.ChoiceField(choices=BackupStatusChoices, required=False)
    details = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = DeviceBackupResult
        nullable_fields = ['details']


class DeviceBackupResultImportForm(NetBoxModelImportForm):
    policy = CSVModelChoiceField(queryset=DeviceBackupPolicy.objects.all())

    class Meta:
        model = DeviceBackupResult
        fields = (
            'policy',
            'backup_date',
            'status',
            'details',
        )
