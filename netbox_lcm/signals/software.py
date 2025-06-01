from django.db.models.signals import post_save
from django.dispatch import receiver
from netbox_lcm.models import SoftwareRelease
from netbox_lcm.choices import SoftwareReleaseStatusChoices

@receiver(post_save, sender=SoftwareRelease)
def enforce_single_target_per_device_type_role(sender, instance, created, **kwargs):
    """
    Ensure only one SoftwareRelease per (device_type, device_role) is marked as TARGET.
    Downgrade others to ACCEPTED. Changelog is auto-captured if triggered by a request.
    """
    if instance.status == SoftwareReleaseStatusChoices.TARGET:
        others = SoftwareRelease.objects.filter(
            device_type=instance.device_type,
            device_role=instance.device_role,
            status=SoftwareReleaseStatusChoices.TARGET
        ).exclude(pk=instance.pk)

        for other in others:
            other.status = SoftwareReleaseStatusChoices.ACCEPTED
            other.save()  # Triggers changelog if done via a request