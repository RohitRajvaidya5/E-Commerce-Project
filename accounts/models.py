from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create Profile automatically when a new User is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save Profile whenever the User is saved."""
    if hasattr(instance, "profile"):
        instance.profile.save()
