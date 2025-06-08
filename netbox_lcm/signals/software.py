from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from netbox_lcm.models import SoftwareRelease, SoftwareReleaseStatus, SoftwareReleaseAssignment
from netbox_lcm.choices import SoftwareReleaseStatusChoices

@receiver(post_save, sender=SoftwareReleaseStatus)
def enforce_single_target_per_device_family_role(sender, instance, created, **kwargs):
    """
    Ensure only one SoftwareReleaseStatus per (devicetype_family, device_role) is marked as TARGET.
    Downgrade others to ACCEPTED. Changelog is auto-captured if triggered by a request.
    """
    if instance.status == SoftwareReleaseStatusChoices.TARGET and instance.devicetype_family:
        others = SoftwareReleaseStatus.objects.filter(
            devicetype_family=instance.devicetype_family,
            device_role=instance.device_role,
            status=SoftwareReleaseStatusChoices.TARGET
        ).exclude(pk=instance.pk)

        for other in others:
            other.status = SoftwareReleaseStatusChoices.ACCEPTED
            other.save()  # Triggers changelog if done via a request

@receiver(post_save, sender=SoftwareReleaseAssignment)
def close_previous_assignment(sender, instance, created, **kwargs):
    if not created:
        return

    # Find other active assignments for the same device (excluding current one)
    prior_assignments = SoftwareReleaseAssignment.objects.filter(
        device=instance.device,
        unassigned_on__isnull=True
    ).exclude(pk=instance.pk)

    for assignment in prior_assignments:
        assignment.unassigned_on = instance.assigned_on or timezone.now()
        assignment.save(update_fields=['unassigned_on'])