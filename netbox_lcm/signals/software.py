from django.db.models.signals import post_save
from django.dispatch import receiver
from netbox_lcm.models import SoftwareRelease
from netbox_lcm.choices import SoftwareReleaseStatusChoices

@receiver(post_save, sender=SoftwareRelease)
def enforce_single_target_per_device_family_role(sender, instance, created, **kwargs):
    """
    Ensure only one SoftwareRelease per (devicetype_family, device_role) is marked as TARGET.
    Downgrade others to ACCEPTED. Changelog is auto-captured if triggered by a request.
    """
    if instance.status == SoftwareReleaseStatusChoices.TARGET and instance.devicetype_family:
        others = SoftwareRelease.objects.filter(
            devicetype_family=instance.devicetype_family,
            device_role=instance.device_role,
            status=SoftwareReleaseStatusChoices.TARGET
        ).exclude(pk=instance.pk)

        for other in others:
            other.status = SoftwareReleaseStatusChoices.ACCEPTED
            other.save()  # Triggers changelog if done via a request