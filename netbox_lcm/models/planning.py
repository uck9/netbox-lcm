from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from netbox_lcm.models import SoftwareRelease, SoftwareReleaseAssignment
from utilities.choices import ChoiceSet

from dcim.models import Device
from netbox.models import PrimaryModel

__all__ = (
    'HardwareLifecyclePlan',
    'SoftwareLifecyclePlan',
    'SoftwareLifecycleTarget',
)


class HardwareLifecyclePlanStatusChoices(ChoiceSet):
    key = 'HardwareLifecyclePlan.status'
    DEFAULT_KEY = 'to_review'

    CHOICES = [
        (DEFAULT_KEY, 'To be reviewed'),
        ('maintain', 'Maintain past EoX'),
        ('replace', 'Replace Device'),
        ('decommission', 'Decommission Device'),
    ]


class HardwareLifecyclePlanTypeChoices(ChoiceSet):
    key = 'HardwareLifecyclePlan.plan_type'
    DEFAULT_KEY = 'to_review'

    CHOICES = [
        (DEFAULT_KEY, 'To be reviewed'),
        ('eox_mgmt', 'EoX Mgmt'),
        ('ops_lc_mgmt', 'Operations Lifecycle Mgmt'),
        ('other', 'Other'),
    ]

class HardwareLifecyclePlanResourceTypeChoices(ChoiceSet):
    key = 'HardwareLifecyclePlan.resource_type'
    DEFAULT_KEY = 'to_review'

    CHOICES = [
        (DEFAULT_KEY, 'To be reviewed'),
        ('bau', 'BAU'),
        ('project', 'Project'),
        ('other', 'Other'),
        ('not_applicable', 'Not Applicable')
    ]

HARDWARE_LIFECYCLE_PLAN_STATUS_DEFAULT = HardwareLifecyclePlanStatusChoices.CHOICES[0][0]
HARDWARE_LIFECYCLE_PLAN_TYPE_DEFAULT = HardwareLifecyclePlanTypeChoices.CHOICES[0][0]
HARDWARE_LIFECYCLE_PLAN_RESOURCE_TYPE_DEFAULT = HardwareLifecyclePlanResourceTypeChoices.CHOICES[0][0]

class HardwareLifecyclePlan(PrimaryModel):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    replacement_device_type = models.ForeignKey('dcim.DeviceType', on_delete=models.CASCADE)
    required_by = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Upgrade to {self.planned_version} (due {self.required_by})"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:hardwarelifecycleplan', args=[self.pk])
    

class HardwareLifecycleActivity(PrimaryModel):
    device = models.OneToOneField(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name='device',
        blank=False,
    )
    plan_type = models.CharField(
        max_length=20, choices=HardwareLifecyclePlanTypeChoices, default=HARDWARE_LIFECYCLE_PLAN_TYPE_DEFAULT
    )
    status = models.CharField(
        max_length=20, choices=HardwareLifecyclePlanStatusChoices, default=HARDWARE_LIFECYCLE_PLAN_STATUS_DEFAULT
    )
    resourcing_type = models.CharField(
        max_length=20, choices=HardwareLifecyclePlanResourceTypeChoices, default=HARDWARE_LIFECYCLE_PLAN_RESOURCE_TYPE_DEFAULT
    )
    required_by = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['plan_type']

    @property
    def name(self):
        return self

    def __str__(self):
        """String representation of HardwareLifecyclePlan."""
        msg = f"Device: {self.device}"
        return msg

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:hardwarelifecycleactivity', args=[self.pk])


class SoftwareLifecyclePlan(PrimaryModel):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    planned_version = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE)
    required_by = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Upgrade to {self.planned_version} (due {self.required_by})"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwarelifecycleplan', args=[self.pk])


class SoftwareLifecycleActivity(PrimaryModel):
    plan = models.ForeignKey(SoftwareLifecyclePlan, on_delete=models.CASCADE, related_name='targets')
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    current_version = models.ForeignKey(SoftwareRelease, on_delete=models.SET_NULL, null=True, blank=True)
    upgrade_started = models.DateTimeField(null=True, blank=True)
    upgraded_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('plan', 'device')

    def is_upgraded(self):
        return self.upgraded_on is not None
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:softwarelifecycleactivity', args=[self.pk])