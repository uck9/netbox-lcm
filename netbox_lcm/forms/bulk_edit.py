from django import forms
from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField

from netbox_lcm.models import SupportContract, SupportSKU, SupportContractAssignment, LicenseAssignment, \
    License, HardwareLifecycle, HardwareLifecyclePlan, Vendor
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import DatePicker


class VendorBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = Vendor
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', )


class SupportSKUBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = SupportSKU
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', )


class SupportContractBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = SupportContract
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', )


class SupportContractAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    contract = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
        required=False,
        selector=True
    )
    sku = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        label=_('SKU'),
        required=False,
        selector=True
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    end = forms.DateField(
        label=_('End date'),
        required=False,
        widget=DatePicker(),
    )
    comments = CommentField()

    model = SupportContractAssignment
    fieldsets = (
        FieldSet('contract', 'sku', 'description', 'end', ),
    )
    nullable_fields = ()


class LicenseBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = License
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', )


class LicenseAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    vendor = DynamicModelChoiceField(
        queryset=SupportSKU.objects.all(),
        label=_('SKU'),
        required=False,
        selector=True
    )
    license = DynamicModelChoiceField(
        queryset=SupportContract.objects.all(),
        label=_('Contract'),
        required=False,
        selector=True
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = LicenseAssignment
    fieldsets = (
        FieldSet('vendor', 'license', 'quantity', 'description', ),
    )
    nullable_fields = ('quantity', )


class HardwareLifecycleBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = HardwareLifecycle
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', )


class HardwareLifecyclePlanBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()
    planned_by = forms.DateField(
        label=_('Completion Date'),
        required=False,
        widget=DatePicker(),
    )

    model = HardwareLifecyclePlan
    fieldsets = (
        FieldSet('description', ),
    )
    nullable_fields = ('description', 'planned_by')