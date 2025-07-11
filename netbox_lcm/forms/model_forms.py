from django import forms
from django.utils.translation import gettext as _

from dcim.models import DeviceType, ModuleType, Manufacturer, Device
from netbox.forms import NetBoxModelForm
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan, Vendor, SupportContract, \
    LicenseAssignment, License, SupportContractAssignment, SupportSKU
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DatePicker


__all__ = (
    'VendorForm',
    'SupportSKUForm',
    'SupportContractForm',
    'SupportContractAssignmentForm',
    'LicenseForm',
    'LicenseAssignmentForm',
    'HardwareLifecycleForm',
    'HardwareLifecyclePlanForm'
)


class VendorForm(NetBoxModelForm):

    class Meta:
        model = Vendor
        fields = ('name', 'description', 'comments', 'tags', )


class SupportSKUForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = SupportSKU
        fields = ('manufacturer', 'sku', 'description', 'comments', 'tags', )


class SupportContractForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )

    class Meta:
        model = SupportContract
        fields = ('vendor', 'contract_id', 'start', 'renewal', 'end', 'description', 'comments', 'tags', )
        widgets = {
            'start': DatePicker(),
            'renewal': DatePicker(),
            'end': DatePicker(),
        }


class SupportContractAssignmentForm(NetBoxModelForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        required=False,
        selector=True,
    )
    sku = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        required=False,
        selector=True,
        label=_('SKU'),
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    license = DynamicModelChoiceField(
        queryset=LicenseAssignment.objects.all(),
        required=False,
        selector=True,
        label=_('License Assignment'),
    )

    class Meta:
        model = SupportContractAssignment
        fields = ('contract', 'sku', 'device', 'license', 'end', 'support_coverage_status', 'description', 'comments', 'tags', )
        widgets = {
            'end': DatePicker(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device', 'license') if self.cleaned_data[field]
        ]

        if len(selected_objects) == 0:
            raise forms.ValidationError({
                'device': "You must select at least a device or license",
                'license': "You must select at least a device or license"
            })

        if self.cleaned_data.get('license') and not self.cleaned_data.get('device'):
            self.cleaned_data['device'] = self.cleaned_data.get('license').device

        if self.cleaned_data.get('license') and self.cleaned_data.get('device'):
            if self.cleaned_data.get('license').device != self.cleaned_data.get('device'):
                raise forms.ValidationError({
                    'device': 'Device assigned to license must match device assignment'
                })


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=False,
    )

    class Meta:
        model = License
        fields = ('manufacturer', 'name', 'description', 'comments', 'tags', )


class LicenseAssignmentForm(NetBoxModelForm):
    vendor = DynamicModelChoiceField(
        queryset=Vendor.objects.all(),
        selector=True,
    )
    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        selector=True,
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )

    class Meta:
        model = LicenseAssignment
        fields = ('vendor', 'license', 'device', 'quantity', 'description', 'start', 'end', 'comments', 'tags', )
        widgets = {
            'start': DatePicker(),
            'end': DatePicker(),
        }


class HardwareLifecycleForm(NetBoxModelForm):
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label=_('Device Type'),
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label=_('Module Type'),
    )

    class Meta:
        model = HardwareLifecycle
        fields = (
            'last_contract_attach', 'last_contract_renewal', 'end_of_sale', 'end_of_maintenance', 'end_of_security', \
            'end_of_support', 'notice_url', 'migration_pid', 'migration_pid_cost', 'migration_pid_cost_currency', \
            'migration_calc_key', 'description', 'comments', 'tags',
        )
        widgets = {
            'last_contract_attach': DatePicker(),
            'last_contract_renewal': DatePicker(),
            'end_of_sale': DatePicker(),
            'end_of_maintenance': DatePicker(),
            'end_of_security': DatePicker(),
            'end_of_support': DatePicker(),
        }

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is DeviceType:
                initial['device_type'] = instance.assigned_object
            elif type(instance.assigned_object) is ModuleType:
                initial['module_type'] = instance.assigned_object
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device_type', 'module_type') if self.cleaned_data[field]
        ]

        if len(selected_objects) > 1:
            raise forms.ValidationError({
                selected_objects[1]: "You can only have a lifecycle for a device or module type"
            })
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None


class HardwareLifecyclePlanForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
            queryset=Device.objects.all(),
            required=True,
            selector=True,
            label=_('Device'),
        )

    class Meta:
        model = HardwareLifecyclePlan
        fields = (
            'device', 'plan_type', 'status', 'resourcing_type', 'completion_by', \
            'description', 'comments', 'tags',
        )
        widgets = {
            'completion_by': DatePicker(),
        }

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('device', ) if self.cleaned_data[field]
        ]

        if len(selected_objects) > 1:
            raise forms.ValidationError({
                selected_objects[1]: "You can only have a single lifecycle plan per device"
            })
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None
