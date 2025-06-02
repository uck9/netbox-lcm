from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from dcim.models import Device, DeviceType, DeviceRole, Manufacturer
from netbox.models import PrimaryModel
from netbox_lcm.choices import SoftwareReleaseStatusChoices


__all__ = (
    'DeviceTypeFamily',
    'SoftwareProduct',
    'SoftwareRelease',
    'SoftwareReleaseAssignment'
)

class DeviceTypeFamily(PrimaryModel):
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.PROTECT,
        related_name='device_type_families'
    )  
    device_types = models.ManyToManyField(
        to='dcim.DeviceType',
        related_name='device_type_families',
        blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"

class SoftwareProduct(PrimaryModel):
    """A software version for a Device, Virtual Machine or Inventory Item."""
    name = models.CharField(max_length=100, unique=True)
    platform = models.ForeignKey(to="dcim.Platform", on_delete=models.CASCADE)
    major_version = models.CharField(max_length=100)
    minor_version = models.CharField(max_length=100)
    alias = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Optional alternative label for this version"
    )
    release_date = models.DateField(null=True, blank=True, verbose_name="Release Date")
    end_of_security_date = models.DateField(null=True, blank=True, verbose_name="End of Security Date")
    end_of_support_date = models.DateField(null=True, blank=True, verbose_name="End of Support Date")
    documentation_url = models.URLField(blank=True, verbose_name="Documentation URL")

    class Meta:
        ordering = ("platform", "major_version", "minor_version", "end_of_support_date", "release_date")
        unique_together = (
            "platform",
            "major_version",
            "minor_version"
        )

    def __str__(self):
        if self.alias:
            return self.alias
        return f"{self.platform.manufacturer.name} {self.platform} {self.name} - {self.major_version}.{self.minor_version}.x"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwareproduct', args=[self.pk])


class SoftwareRelease(PrimaryModel):
    product = models.ForeignKey(
        SoftwareProduct, 
        on_delete=models.CASCADE, 
        related_name='releases'
    )
    devicetype_family = models.ForeignKey(
        to='DeviceTypeFamily', 
        on_delete=models.PROTECT
    )
    version = models.CharField(max_length=100)
    version_alias = models.CharField(max_length=100)
    device_role = models.ForeignKey(
        DeviceRole, 
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=SoftwareReleaseStatusChoices,
        default=SoftwareReleaseStatusChoices.ACCEPTED
    )
    notes = models.CharField(
        verbose_name=_('notes'),
        max_length=200,
        blank=True
    )

    @property
    def release_status(self):
        return self.get_status_display()

    class Meta:
        unique_together = ('product', 'version', 'devicetype_family', 'device_role')
        ordering = ['product__name', 'version']

    def __str__(self):
        role = f" for {self.device_role}" if self.device_role else " (Default)"
        return f"{self.version} [Model: {self.devicetype_family}, Role:{role}]"

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwarerelease', args=[self.pk])


class SoftwareReleaseAssignment(PrimaryModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    release = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE)
    assigned = models.DateTimeField(auto_now_add=True)
    currently_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-assigned']
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'release'],
                name='unique_device_release_history'
            )
        ]

    def __str__(self):
        return f"{self.device} => {self.release}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwarereleaseassignment', args=[self.pk])
    
