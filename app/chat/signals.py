from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import User, PFP
from .models import PFP


@receiver(post_save, sender=User)
def create_user_pfp(sender, instance, created, **kwargs):
    """Create pfp record on user creation."""
    if created:
        PFP.objects.create(user=instance)


@receiver(pre_save, sender=PFP)
def delete_old_pfp(sender, instance, **kwargs):
    """Delete old profile picture before saving a new one."""
    if instance.pk:
        old_pfp = None
        try:
            old_pfp = PFP.objects.get(pk=instance.pk).image
        except PFP.DoesNotExist:
            pass
        if old_pfp and old_pfp != instance.image:
            if default_storage.exists(old_pfp.name):
                default_storage.delete(old_pfp.name)


@receiver(post_delete, sender=PFP)
def delete_pfp_file(sender, instance, **kwargs):
    """Delete profile picture file when the PFP instance is deleted."""
    if instance.image and default_storage.exists(instance.image.name):
        default_storage.delete(instance.image.name)
