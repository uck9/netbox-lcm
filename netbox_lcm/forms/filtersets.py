from django import forms
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms import CharField, DateField, NullBooleanField, Select

from dcim.choices import DeviceStatusChoices
from dcim.models import Device, DeviceType, Manufacturer, Site
from tenancy.models import Tenant, TenantGroup
from netbox_lcm.choices.contract import SupportCoverageStatusChoices
from netbox.forms import NetBoxModelFilterSetForm
from netbox_lcm.models import HardwareLifecycle, HardwareLifecyclePlan, SupportContract, \
    Vendor, License, LicenseAssignment, SupportContractAssignment, SupportSKU
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import APISelectMultiple, DatePicker


__all__ = (
    'HardwareLifecycleFilterForm',
    'HardwareLifecyclePlanFilterForm',
    'SupportSKUFilterForm',
    'SupportContractFilterForm',
    'VendorFilterForm',
    'LicenseFilterForm',
    'LicenseAssignmentFilterForm',
    'SupportContractAssignmentFilterForm',
    'DeviceLifecycleFilterForm'
)


class HardwareLifecycleFilterForm(NetBoxModelFilterSetForm):
    model = HardwareLifecycle
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('assigned_object_type_id', 'support_expired', name=_('Hardware')),
        FieldSet('end_of_sale__lt', 'end_of_maintenance__lt', 'end_of_security__lt', 'last_contract_attach__lt', \
            'last_contract_renewal__lt', 'end_of_support__lt', name=_('Dates'))
    )

    assigned_object_type_id = DynamicModelMultipleChoiceField(
        queryset=ContentType.objects.filter( \
            Q(app_label='dcim', model='devicetype') | Q(app_label='dcim', model='moduletype')),
        required=False,
        label=_('Object Type'),
        widget=APISelectMultiple(
            api_url='/api/extras/content-types/',
        )
    )
    end_of_sale__lt = DateField(
        required=False,
        label=_('End of sale before'),
        widget=DatePicker,
    )
    end_of_maintenance__lt = DateField(
        required=False,
        label=_('End of maintenance before'),
        widget=DatePicker,
    )
    end_of_security__lt = DateField(
        required=False,
        label=_('End of security before'),
        widget=DatePicker,
    )
    last_contract_attach__lt = DateField(
        required=False,
        label=_('Last contract attach before'),
        widget=DatePicker,
    )
    last_contract_renewal__lt = DateField(
        required=False,
        label=_('Last contract renewal before'),
        widget=DatePicker,
    )
    end_of_support__lt = DateField(
        required=False,
        label=_('End of support before'),
        widget=DatePicker,
    )
    support_expired = NullBooleanField(
        required=False,
        label=_("Vendor Support Expired"),
        widget=Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
    tag = TagFilterField(model)


class HardwareLifecyclePlanFilterForm(NetBoxModelFilterSetForm):
    model = HardwareLifecyclePlan
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('device_id', name=_('Assignment')),
        FieldSet('completion_by__lt', name=_('Dates'))
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Devices'),
    )
    completion_by__lt = DateField(
        required=False,
        label=_('Planned completion before'),
        widget=DatePicker,
    )
    tag = TagFilterField(model)


class SupportSKUFilterForm(NetBoxModelFilterSetForm):
    model = SupportSKU
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag', 'manufacturer_id'),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label=_('Manufacturer'),
    )
    tag = TagFilterField(model)


class SupportContractFilterForm(NetBoxModelFilterSetForm):
    model = SupportContract
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('vendor_id', name='Purchase Information'),
    )
    vendor_id = DynamicModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
        label=_('Vendor'),
    )
    tag = TagFilterField(model)


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
    )
    tag = TagFilterField(model)


class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('manufacturer_id', name='License Information'),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label=_('Manufacturer'),
    )
    tag = TagFilterField(model)


class SupportContractAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = SupportContractAssignment
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('support_coverage_status', name='Coverage'),
        FieldSet('contract_id', 'device_id', 'license_id', 'sku_id', 'device_status', name='Assignment'),
        FieldSet('end__lt', name='Dates'),
    )
    contract_id = DynamicModelMultipleChoiceField(
        queryset=SupportContract.objects.all(),
        required=False,
        selector=True,
        label=_('Contracts'),
    )
    license_id = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        selector=True,
        label=_('Licenses'),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Devices'),
    )
    device_status = forms.MultipleChoiceField(
        label=_('Device Status'),
        choices=DeviceStatusChoices,
        required=False
    )
    sku_id = DynamicModelMultipleChoiceField(
        queryset=SupportSKU.objects.all(),
        required=False,
        selector=True,
        label=_('Support SKU'),
    )
    end__lt = DateField(
        required=False,
        label=_('Contract End before'),
        widget=DatePicker,
    )
    support_coverage_status = forms.MultipleChoiceField(
        label=_('Support Coverage Status'),
        choices=SupportCoverageStatusChoices,
        required=False
    )
    tag = TagFilterField(model)


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('license_id', 'vendor_id', 'device_id', name='Assignment'),
        FieldSet('end__lt', name=('Dates')),
    )
    license_id = DynamicModelMultipleChoiceField(
        queryset=License.objects.all(),
        required=False,
        selector=True,
        label=_('Licenses'),
    )
    vendor_id = DynamicModelMultipleChoiceField(
        queryset=Vendor.objects.all(),
        required=False,
        selector=True,
        label=_('Vendors'),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Devices'),
    )
    end__lt = DateField(
        required=False,
        label=_('License End before'),
        widget=DatePicker,
    )
    tag = TagFilterField(model)


class DeviceLifecycleFilterForm(NetBoxModelFilterSetForm):
    model = Device
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('site', 'tenant_group', 'tenant', name='Organisation Information'),
        FieldSet('status', 'manufacturer', 'device_type', 'has_primary_ip', name='Device Information'),
        FieldSet('has_support_contract', 'support_contract_end_before', 
            'hw_eosec_before', name='Lifecyle Information'),
    )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    tenant_group = DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label='Tenant Group'
    )
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        required=False
    )
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False
    )
    device_type = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False
    )
    has_primary_ip = NullBooleanField(
        required=False,
        label=_("Has Primary IP"),
        widget=Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
    has_support_contract = NullBooleanField(
        required=False,
        label=_("Has Support Contract"),
        widget=Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
    support_contract_end_before = DateField(
        required=False, 
        label="Support Contract ends before",
        widget=DatePicker,
    )
    hw_eosec_before = DateField(
        required=False, 
        label="HW EoVSS before",
        widget=DatePicker,
    )