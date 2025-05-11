from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

# uplading user files
def user_directory(instance,filename):
    return f'user{instance.user.id}/{filename}'


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)

    def get_url_tag(self):
        return reverse('tags',args=[self.slug])

    def save(self, *args, **kwargs):
    # Auto-generate the slug from the title when saving the object
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory)
    caption = models.CharField(max_length=1000)
    posted = models.DateField(auto_now_add='true')
    tags = models.ManyToManyField(Tag,related_name ='tags')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Follow(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name ='following')    
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name ='follower') 
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateField()

@receiver(post_save, sender=Post)
def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        post = instance 
        user = post.user

        followers = Follow.objects.filter(following=user) 

        for follower in followers:
            stream = Stream(user=follower.follower, post=post, date=post.posted, following=user)
            stream.save()


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    
class Post_save(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)    
    post = models.ForeignKey(Post, on_delete = models.SET_NULL, null=True)   