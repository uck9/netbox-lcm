from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from dcim.models import Device, DeviceType, DeviceRole, Manufacturer
from netbox.models import PrimaryModel
from netbox_lcm.choices import SoftwareReleaseStatusChoices, CVESeverityChoices


__all__ = (
    'DeviceTypeFamily',
    'SoftwareProduct',
    'SoftwareRelease',
    'SoftwareReleaseStatus',
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
        return f"{self.name}"

class SoftwareProduct(PrimaryModel):
    """A software version for a Device, Virtual Machine or Inventory Item."""
    name = models.CharField(max_length=100)
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
    notes = models.CharField(
        verbose_name=_('notes'),
        max_length=200,
        blank=True
    )

    class Meta:
        unique_together = ('product', 'version', 'devicetype_family')
        ordering = ['product__name', 'version']

    def __str__(self):
        return f"{self.version} [Family: {self.devicetype_family}]"

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwarerelease', args=[self.pk])


class SoftwareReleaseStatus(PrimaryModel):
    release = models.ForeignKey('SoftwareRelease', on_delete=models.CASCADE, related_name='status_assignments')
    device_role = models.ForeignKey(DeviceRole, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, 
        choices=SoftwareReleaseStatusChoices, 
        default=SoftwareReleaseStatusChoices.ACCEPTED
    )

    class Meta:
        verbose_name = "Software Releases Statuse"
        unique_together = ('release', 'device_role')
        ordering = ['release', 'device_role']

    def __str__(self):
        role = self.device_role.name if self.device_role else 'Default'
        return f"{self.release} [{role}]: {self.get_status_display()}"

    def get_effective_status(release, device_role):
        return (
            SoftwareReleaseStatus.objects.filter(release=release, device_role=device_role).first() or
            SoftwareReleaseStatus.objects.filter(release=release, device_role=None).first()
        )


class SoftwareReleaseAssignment(PrimaryModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    release = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE)
    assigned_on = models.DateTimeField(auto_now_add=True)
    unassigned_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-assigned_on']
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


class SoftwareCVE(PrimaryModel):
    """SoftwareCVE is the representation of a cve vulnerability record."""

    name = models.CharField(max_length=100, blank=False, unique=True)
    published_date = models.DateField(verbose_name="Published Date")
    last_modified_date = models.DateField(null=True, blank=True, verbose_name="Last Modified Date")
    documentation_url = models.URLField()
    description = models.TextField(blank=True, default="")
    cve_severity = models.CharField(
        max_length=100, choices=CVESeverityChoices, default=CVESeverityChoices.NONE,
    )
    agreed_severity = models.CharField(
        max_length=100, choices=CVESeverityChoices, default=CVESeverityChoices.NONE,
        verbose_name="Agreed Severity"
    )
    cvss = models.FloatField(blank=True, null=True, verbose_name="CVSS Base Score")
    cvss_v2 = models.FloatField(blank=True, null=True, verbose_name="CVSSv2 Score")
    cvss_v3 = models.FloatField(blank=True, null=True, verbose_name="CVSSv3 Score")
    fix = models.CharField(max_length=255, blank=True, default="")
    workaround_avail = models.BooleanField(default=True)
    comments = models.TextField(blank=True, default="")
    affected_softwares = models.ManyToManyField(
        to="SoftwareRelease", related_name="corresponding_cves", blank=True
    )
    

    class Meta:
        """Meta attributes for the class."""

        verbose_name = "Software CVE"

        ordering = ("agreed_severity", "name")

    def __str__(self):
        """String representation of the model."""
        return f"{self.name}"

