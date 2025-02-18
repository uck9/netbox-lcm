from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse

from netbox.models import PrimaryModel


__all__ = (
    'License',
    'LicenseAssignment'
)


class License(PrimaryModel):
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        related_name='licenses',
    )
    name = models.CharField(max_length=100)

    clone_fields = (
        'manufacturer',
    )
    prerequisite_models = (
        'dcim.Manufacturer',
    )

    class Meta:
        ordering = ['manufacturer', 'name']
        constraints = (
            models.UniqueConstraint(
                'manufacturer', Lower('name'),
                name='%(app_label)s_%(class)s_unique_manufacturer_name',
                violation_error_message="SKU name must be unique per manufacturer."
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:license', args=[self.pk])


class LicenseAssignment(PrimaryModel):
    license = models.ForeignKey(
        to='netbox_lcm.License',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    vendor = models.ForeignKey(
        to='netbox_lcm.Vendor',
        on_delete=models.CASCADE,
        related_name='licenses',
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='licenses',
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
    )
    start = models.DateField(
        null=True, 
        blank=True
    )
    end = models.DateField(
        null=True, 
        blank=True
    )

    clone_fields = (
        'vendor', 'license',
    )
    prerequisite_models = (
        'netbox_lcm.License',
        'netbox_lcm.Vendor',
        'dcim.Device',
    )

    class Meta:
        ordering = ['license', 'device']
        constraints = (
            models.UniqueConstraint(
                'license', 'vendor', 'device',
                name='%(app_label)s_%(class)s_unique_license_vendor_device',
                violation_error_message="License assignment must be unique."
            ),
        )

    def __str__(self):
        if self.device is None:
            return f'{self.license.name}'
        return f'{self.device.name}: {self.license.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:licenseassignment', args=[self.pk])

    @property
    def name(self):
        if self.device is None:
            return None
        return f'{self.device.name}'

    @property
    def serial(self):
        if self.device is None:
            return None
        return f'{self.device.serial}'

    @property
    def device_type(self):
        if self.device is None:
            return None
        return self.device.device_type

    @property
    def status(self):
        if self.device is None:
            return None
        return self.device.status
