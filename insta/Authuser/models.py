from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return "default-profile.png"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update UserProfile when a User is created or saved.
    """    
    try:
        user_profile = instance.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    if created or user_profile is None:
        # If the user is created or UserProfile does not exist, create a UserProfile instance
        UserProfile.objects.get_or_create(user=instance)
    else:
        # If the user is saved (updated) and UserProfile exists, update it
        user_profile.save()


# Create your models here.
