from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox_lcm.choices import SupportCoverageStatusChoices
from dcim.choices import DeviceStatusChoices
from netbox.models import PrimaryModel


__all__ = (
    'Vendor',
    'SupportSKU',
    'SupportContract',
    'SupportContractAssignment',
)


class Vendor(PrimaryModel):
    name = models.CharField(max_length=100)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Vendor must be unique."
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:vendor', args=[self.pk])


class SupportSKU(PrimaryModel):
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        related_name='skus',
    )
    sku = models.CharField(max_length=100)

    clone_fields = (
        'manufacturer',
    )
    prerequisite_models = (
        'dcim.Manufacturer',
    )

    class Meta:
        ordering = ['manufacturer', 'sku']
        constraints = (
            models.UniqueConstraint(
                'manufacturer', Lower('sku'),
                name='%(app_label)s_%(class)s_unique_manufacturer_sku',
                violation_error_message="SKU must be unique per manufacturer."
            ),
        )

    def __str__(self):
        return f'{self.sku}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:supportsku', args=[self.pk])


class SupportContract(PrimaryModel):
    vendor = models.ForeignKey(
        to='netbox_lcm.Vendor',
        on_delete=models.SET_NULL,
        related_name='contracts',
        null=True,
        blank=True,
    )
    contract_id = models.CharField(max_length=100)
    start = models.DateField(null=True, blank=True)
    renewal = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    clone_fields = (
        'vendor', 'start', 'renewal', 'end'
    )
    prerequisite_models = (
        'netbox_lcm.Vendor',
    )

    class Meta:
        ordering = ['contract_id']
        constraints = (
            models.UniqueConstraint(
                'vendor', Lower('contract_id'),
                name='%(app_label)s_%(class)s_unique_vendor_contract_id',
                violation_error_message="Contract must be unique per vendor."
            ),
        )

    def __str__(self):
        return f'{self.contract_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:supportcontract', args=[self.pk])


class SupportContractAssignment(PrimaryModel):
    contract = models.ForeignKey(
        to='netbox_lcm.SupportContract',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assignments',
    )
    sku = models.ForeignKey(
        to='netbox_lcm.SupportSKU',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assignments',
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contracts',
    )
    license = models.ForeignKey(
        to='netbox_lcm.LicenseAssignment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contracts',
    )
    end = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date'),
        help_text=_('A unique end date varying from the contract')
    )
    support_coverage_status = models.CharField(
        max_length=32,
        choices=SupportCoverageStatusChoices,
        blank=True,
        help_text=_("Support Coverage Status")
    )

    clone_fields = (
        'contract', 'sku', 'end',
    )
    prerequisite_models = (
        'netbox_lcm.SupportContract',
        'netbox_lcm.SupportSKU',
        'netbox_lcm.License',
        'dcim.Device',
    )

    class Meta:
        ordering = ['contract', 'device', 'license']
        constraints = ()

    def __str__(self):
        if self.license and self.device:
            return f'{self.device} ({self.license}): {self.contract.contract_id if self.contract else self.get_support_coverage_status_display()}'
        return f'{self.device}: {self.contract.contract_id if self.contract else self.get_support_coverage_status_display()}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:supportcontractassignment', args=[self.pk])

    @property
    def end_date(self):
        if self.end:
            return self.end
        return self.contract.end

    def get_device_status_color(self):
        if self.device is None:
            return
        return DeviceStatusChoices.colors.get(self.device.status)

    def get_support_coverage_status_color(self):
        if self.device is None:
            return
        return SupportCoverageStatusChoices.colors.get(self.support_coverage_status)

    @property
    def assignment_type(self):
        if self.license:
            return 'license'
        else:
            return 'device'
    

    def clean(self):
        if self.contract:
            if not self.support_coverage_status == SupportCoverageStatusChoices.VENDOR_CONTRACT_ATTACHED:
                raise ValidationError({
                    'support_coverage_status': _('Contract can only be specified when "Supported - Vendor Contract Attached" is selected.')
                })
            else:
                self.support_coverage_status = SupportCoverageStatusChoices.VENDOR_CONTRACT_ATTACHED
        elif not self.contract:
            if not self.support_coverage_status:
                raise ValidationError({
                    'support_coverage_status': _('A reason must be specified if no contract is assigned.')
                })
            elif self.support_coverage_status == SupportCoverageStatusChoices.VENDOR_CONTRACT_ATTACHED:
                raise ValidationError({
                    'support_coverage_status': _('"Supported - Vendor Contract Attached" can only be used when a contract is assigned.')
                })

        # Uniqueness constraints
        qs = SupportContractAssignment.objects.filter(
            device=self.device, license=self.license, sku=self.sku
        ).exclude(pk=self.pk)

        if self.device and self.license and self.contract and qs.filter(contract=self.contract).exists():
            raise ValidationError('Device or License must be unique')
        elif self.device and not self.license and qs.filter(contract=self.contract).exists():
            raise ValidationError('Device must be unique')
        elif not self.device and self.license and qs.filter(contract=self.contract).exists():
            raise ValidationError('License must be unique')
