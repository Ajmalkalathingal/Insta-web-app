from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta


from main.models import Follow


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='stories/',null=True)  # Accepts images/videos
    caption = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    expires_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
        
		

class StoryStream(models.Model):
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	story = models.ManyToManyField(Story, related_name='storiess')
	date = models.DateTimeField(auto_now_add=True)

