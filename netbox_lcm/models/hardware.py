from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from dcim.models import DeviceType, ModuleType, Device, Module
from netbox.models import PrimaryModel
from utilities.choices import ChoiceSet

from netbox_lcm.constants import HARDWARE_LIFECYCLE_MODELS


__all__ = (
    'HardwareLifecycle',
)


class CurrencyChoices(ChoiceSet):
    key = 'HardwaeLifecycle.migration_pid_cost_currency'
    CURRENCY_USD = 'usd'

    CHOICES = [
        (CURRENCY_USD, 'USD'),
        ('aud', 'AUD'),
    ]

CURRENCY_DEFAULT = CurrencyChoices.CHOICES[0][0]


class HardwareLifecycle(PrimaryModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=HARDWARE_LIFECYCLE_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )

    end_of_sale = models.DateField()
    end_of_maintenance = models.DateField(blank=True, null=True)
    end_of_security = models.DateField(blank=True, null=True)
    last_contract_attach = models.DateField(blank=True, null=True)
    last_contract_renewal = models.DateField(blank=True, null=True)
    end_of_support = models.DateField()

    notice_url = models.URLField(blank=True)
    migration_pid = models.CharField(max_length=100, blank=True, null=True)
    migration_pid_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    migration_pid_cost_currency = models.CharField(max_length=3, choices=CurrencyChoices, default=CURRENCY_DEFAULT)


    class Meta:
        ordering = ['assigned_object_type']
        constraints = (
            models.UniqueConstraint(
                'assigned_object_type', 'assigned_object_id',
                name='%(app_label)s_%(class)s_unique_object',
                violation_error_message="Objects must be unique."
            ),
        )

    @property
    def name(self):
        return self

    def __str__(self):
        if not self.assigned_object:
            return f'{self.pk}'
        elif isinstance(self.assigned_object, ModuleType):
            return f'Module Type: {self.assigned_object.model}'
        return f'Device Type: {self.assigned_object.model}'

    @property
    def assigned_object_count(self):
        if isinstance(self.assigned_object, DeviceType):
            return Device.objects.filter(device_type=self.assigned_object).count()
        return Module.objects.filter(module_type=self.assigned_object).count()

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:hardwarelifecycle', args=[self.pk])
