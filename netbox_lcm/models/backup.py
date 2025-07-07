from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext as _
from datetime import date, timedelta

from netbox_lcm.choices import BackupSystemChoices, BackupStatusChoices
from netbox.models import PrimaryModel
from dcim.models import Device

__all__ = (
    'DeviceBackupPolicy',
    'DeviceBackupResult',
)

class DeviceBackupPolicy(PrimaryModel):
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='backup_policies'
    )
    enabled = models.BooleanField(default=True)
    critical = models.BooleanField(
        default=False,
        verbose_name="Evaluate Backup Status",
        help_text="Critical Device that MUST have successful daily backup"
        )
    evaluate_status = models.BooleanField(
        default=True,
        verbose_name="Evaluate Backup Status",
        help_text="If set as False, this policy will not be included in compliance or backup success rate evaluations."
    )
    backup_system = models.CharField(
        max_length=50,
        choices=BackupSystemChoices.choices,
        default=BackupSystemChoices.NONE
    )
    destination = models.TextField(
        blank=True,
        help_text="Path, URL, or location where backups are stored."
    )
    method = models.CharField(
        max_length=255,
        blank=True,
        help_text="Manual method or command used if not automated."
    )
    notes = models.TextField(blank=True)

    def get_backup_health_score(self, days=30):
        if not self.enabled or not self.evaluate_status:
            return None

        cutoff = date.today() - timedelta(days=days)
        results = self.results.filter(backup_date__gte=cutoff)

        total = results.count()
        success = results.filter(status='success').count()
        success_rate = (success / total) * 100 if total > 0 else 0

        last_success = results.filter(status='success').order_by('-backup_date').first()
        if last_success:
            days_since = (date.today() - last_success.backup_date).days

            if self.critical:
                # Critical backups degrade faster: 20 pts/day after 1 day
                recency_score = max(0, 100 - max(0, days_since - 1) * 20)
            else:
                # Normal backups degrade 10 pts/day after 1 day
                recency_score = max(0, 100 - max(0, days_since - 1) * 10)
        else:
            recency_score = 0

        # Combined weighted score
        score = round((0.6 * success_rate) + (0.4 * recency_score), 1)
        return score

    class Meta:
        verbose_name = "Device Backup Policy"
        verbose_name_plural = "Device Backup Policies"
        constraints = (
            models.UniqueConstraint(
                'device', 'backup_system',
                name='%(app_label)s_%(class)s_unique_device_backupsystem',
                violation_error_message="Assigned Backup Systems must be unique."
            ),
        )

    def __str__(self):
        return f"{self.device.name} [{self.get_backup_system_display()}]"

    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:devicebackuppolicy', args=[self.pk])

class DeviceBackupResult(PrimaryModel):
    policy = models.ForeignKey(
        to=DeviceBackupPolicy,
        on_delete=models.CASCADE,
        related_name='results'
    )
    backup_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BackupStatusChoices.choices,
        default=BackupStatusChoices.UNKNOWN
    )
    details = models.TextField(blank=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                'policy', 'backup_date',
                name='%(app_label)s_%(class)s_unique_policy_backupdate',
                violation_error_message="Backup Date must be unique per backup policy."
            ),
        )
        ordering = ['-backup_date']

    def __str__(self):
        return f"{self.policy} @ {self.backup_date}: {self.get_status_display()}"

    @property
    def device(self):
        return self.policy.device
    
    @property
    def backup_health_label(self):
        score = self.get_backup_health_score()
        if score is None:
            return "Excluded"
        elif score >= 90:
            return "Healthy"
        elif score >= 70:
            return "Warning"
        else:
            return "At Risk"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:devicebackupresult', args=[self.pk])