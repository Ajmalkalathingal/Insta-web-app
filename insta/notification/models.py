from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Post, Follow,Comments,Like

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',null=True, blank=True)
    notification_type = models.CharField(max_length=20)  # Example: 'post', 'follow', 'like', 'comment'
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post

        # Create a notification for the user who owns the post
        Notification.objects.create(
            user=post.user,
            sender=instance.user,
            notification_type='like',
            post=post
        )

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.following, sender=instance.follower, notification_type='follow', follow=instance)
        

@receiver(post_save, sender=Comments)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post

        # Create a notification for the user who owns the post
        Notification.objects.create(
            user=post.user,
            sender=instance.user,
            notification_type='comment',
            post=post,
            comment=instance
        )
