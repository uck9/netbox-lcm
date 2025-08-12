# netbox_lcm/models/external.py
from django.db import models, transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from netbox_lcm.choices import ExternalAssessmentStatusChoices
from netbox.models import PrimaryModel


__all__ = (
    'ExternalAssessmentType',
    'ExternalAssessment',
)


class ExternalAssessmentType(PrimaryModel):
    """
    Optional registry for types (e.g., 'nac', 'config', 'vuln').
    Lets you define defaults & UI behavior per type.
    """
    slug = models.SlugField(primary_key=True, max_length=64)
    label = models.CharField(max_length=128)
    default_retention_days = models.PositiveIntegerField(default=90)
    higher_is_better = models.BooleanField(default=True)
    ui_badge = models.CharField(max_length=32, default="default")

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.label or self.slug
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:externalassessmenttype', args=[self.pk])


class ExternalAssessment(PrimaryModel):
    """
    Generic, not-change-logged container for externally generated assessments.
    Target can be Device, Interface, VM, Site, etc.
    """
    # What family/type of assessment this is
    assessment_type = models.ForeignKey(
        ExternalAssessmentType,
        to_field='slug',
        db_column='assessment_type',
        on_delete=models.PROTECT
    )

    # Generic target
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    target_id = models.PositiveBigIntegerField(db_index=True)
    target = GenericForeignKey("target_type", "target_id")

    # Provenance/run
    source = models.CharField(max_length=128, db_index=True, help_text="Producer system")
    source_run_id = models.CharField(max_length=128, blank=True, null=True, help_text="Batch/run identifier")
    external_reference = models.CharField(max_length=256, blank=True, null=True, help_text="Upstream PK/ref")

    # Timing
    observed_at = models.DateTimeField(db_index=True, help_text="When data was measured")
    expires_at = models.DateTimeField(blank=True, null=True)
    retention_days = models.PositiveIntegerField(default=90)

    # Result
    status = models.CharField(
        max_length=16,
        choices=ExternalAssessmentStatusChoices,
        default=ExternalAssessmentStatusChoices.UNKNOWN,
        db_index=True,
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="0–100 if applicable")
    summary = models.CharField(max_length=255, blank=True, default="")
    details = models.JSONField(default=dict, blank=True)
    external_url = models.URLField(blank=True, null=True)

    # Bookkeeping
    is_latest = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-observed_at"]
        indexes = [
            models.Index(fields=["assessment_type", "target_type", "target_id", "-observed_at"]),
            models.Index(fields=["source", "observed_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment_type", "target_type", "target_id"],
                condition=models.Q(is_latest=True),
                name="uniq_latest_per_type_target",
            ),
        ]

    # models/external.py
    def __str__(self):
        obj = self.target  # dereferences the GFK (one DB query)
        label = str(obj) if obj else f"{self.target_type.app_label}.{self.target_type.model}:{self.target_id}"
        return f"{self.assessment_type} [{self.status}] on {label} @ {self.observed_at:%Y-%m-%d %H:%M}"


    @classmethod
    def mark_latest_for(cls, assessment_type: str, target_type_id: int, target_id: int):
        """
        Flip is_latest so only the newest observed_at record is marked latest.
        Use inside a transaction.
        """
        qs = cls.objects.filter(
            assessment_type=assessment_type,
            target_type_id=target_type_id,
            target_id=target_id,
        ).order_by("-observed_at", "-id")

        newest = qs.first()
        if not newest:
            return

        cls.objects.filter(
            assessment_type=assessment_type,
            target_type_id=target_type_id,
            target_id=target_id,
            is_latest=True,
        ).exclude(pk=newest.pk).update(is_latest=False)

        if not newest.is_latest:
            newest.is_latest = True
            newest.save(update_fields=["is_latest", "updated"])

    def save(self, *args, **kwargs):
        """
        Optional: eagerly maintain is_latest with minimal contention.
        For high-throughput bulk ingests, you can disable this and run the job instead.
        """
        with transaction.atomic():
            super().save(*args, **kwargs)
            # Best-effort: set this instance as latest if it's newer than current latest
            type_id = self.target_type_id
            ExternalAssessment.mark_latest_for(self.assessment_type, type_id, self.target_id)
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_lcm:externalassessment', args=[self.pk])
