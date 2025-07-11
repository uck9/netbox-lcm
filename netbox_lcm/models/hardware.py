from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.conf import settings

from dcim.models import DeviceType, ModuleType, Device, Module
from netbox.models import PrimaryModel
from utilities.choices import ChoiceSet

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from netbox_lcm.constants import HARDWARE_LIFECYCLE_MODELS


__all__ = (
    'HardwareLifecycle',
    'HardwareLifecyclePlan',
)


class CurrencyChoices(ChoiceSet):
    key = 'HardwareLifecycle.migration_pid_cost_currency'
    CURRENCY_USD = 'usd'

    CHOICES = [
        (CURRENCY_USD, 'USD'),
        ('aud', 'AUD'),
    ]


class MigrationCalcKeyChoices(ChoiceSet):
    key = 'HardwareLifecycle.migration_calc__key'
    DEFAULT_KEY = 'security'

    CHOICES = [
        (DEFAULT_KEY, 'End of Security'),
        ('support', 'End of Support'),
    ]


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


CURRENCY_DEFAULT = CurrencyChoices.CHOICES[0][0]
MIGRATION_CALC_KEY_DEFAULT = MigrationCalcKeyChoices.CHOICES[0][0]
HARDWARE_LIFECYCLE_PLAN_STATUS_DEFAULT = HardwareLifecyclePlanStatusChoices.CHOICES[0][0]
HARDWARE_LIFECYCLE_PLAN_TYPE_DEFAULT = HardwareLifecyclePlanTypeChoices.CHOICES[0][0]
HARDWARE_LIFECYCLE_PLAN_RESOURCE_TYPE_DEFAULT = HardwareLifecyclePlanResourceTypeChoices.CHOICES[0][0]
MIGRATION_CALC_MONTH = settings.PLUGINS_CONFIG["netbox_lcm"].get("hw_lcm_migration_calc_month", 6)


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

    notice_url = models.URLField(blank=True)
    end_of_sale = models.DateField()
    end_of_maintenance = models.DateField(blank=True, null=True)
    end_of_security = models.DateField(blank=True, null=True)
    last_contract_attach = models.DateField(blank=True, null=True)
    last_contract_renewal = models.DateField(blank=True, null=True)
    end_of_support = models.DateField()
    migration_pid = models.CharField(max_length=100, blank=True, null=True)
    migration_pid_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    migration_pid_cost_currency = models.CharField(
        max_length=3, choices=CurrencyChoices, default=CURRENCY_DEFAULT)
    migration_calc_key = models.CharField(
        max_length=10, choices=MigrationCalcKeyChoices, default=MIGRATION_CALC_KEY_DEFAULT)

    class Meta:
        ordering = ['assigned_object_type', 'end_of_support']
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
    def is_supported(self):
        """
        Return False if the current date is greater than the selected EoX date.

        If the current date is less than or equal to the end of support date, return True.
        """
        today = datetime.today().date()
        # Find the Key we're using
        if (getattr(self, "migration_calc_key") == "support"):
            return today < getattr(self, "end_of_support")
        else:
            return today < getattr(self, "end_of_security")

    @property
    def assigned_object_count(self):
        if isinstance(self.assigned_object, DeviceType):
            return Device.objects.filter(device_type=self.assigned_object).count()
        return Module.objects.filter(module_type=self.assigned_object).count()

    @property
    def days_to_vendor_eos(self):
        """
        Return True if the current date is greater than the vendor EoS date.

        If the current date is less than or equal to the end of support date, return False.
        """
        today = datetime.today().date()
        if (getattr(self, "migration_calc_key") == "support"):
            end_of_date = getattr(self, "end_of_support")
        else:
            end_of_date = getattr(self, "end_of_security")
        return (self.end_of_support - today).days

    @property
    def calc_replacement_year(self):
        # Work out the date we're referencing
        if (getattr(self, "migration_calc_key") == "support"):
            end_of_date = getattr(self, "end_of_support")
        else:
            end_of_date = getattr(self, "end_of_security")

        if (end_of_date.month <= MIGRATION_CALC_MONTH):
            replace_date = end_of_date - relativedelta(years=1)
            replace_year = replace_date.year
        else:
            replace_date = end_of_date
            replace_year = replace_date.year
        return replace_year

    @property
    def calc_budget_year(self):
        # Find the Key we're using
        if (getattr(self, "migration_calc_key") == "support"):
            end_of_date = getattr(self, "end_of_support")
        else:
            end_of_date = getattr(self, "end_of_security")

        if (end_of_date.month <= MIGRATION_CALC_MONTH):
            budget_date = end_of_date - relativedelta(years=2)
            budget_year = budget_date.year
        else:
            budget_date = end_of_date - relativedelta(years=1)
            budget_year = budget_date.year
        return budget_year

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:hardwarelifecycle', args=[self.pk])


class HardwareLifecyclePlan(PrimaryModel):
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
    completion_by = models.DateField(blank=True, null=True)

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
        return reverse('plugins:netbox_lcm:hardwarelifecycleplan', args=[self.pk])
