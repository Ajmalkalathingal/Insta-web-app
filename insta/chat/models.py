from django.db import models
from django.contrib.auth.models import User



# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
#     receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,related_name='receiver')
#     message = models.TextField(null=True, blank=True)
#     theard_name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='messaged_image',null=True, blank=True)
#     date = models.DateTimeField(auto_now=True)
#     is_read = models.BooleanField(default=False)    

#     def __str__(self) -> str:
#         return f"{self.message or self.image}"

class ChatGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='chat_groups')

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,blank=True,related_name='receiver')
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='group_messages')
    
    message = models.TextField(null=True, blank=True)
    theard_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='messaged_image', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -> {self.receiver or self.group}: {self.message or 'Image'}"


class Notificaton(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_notification')
    receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,related_name='receiver_notification')
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE,null=True)
    is_seen = models.BooleanField(default=False) 


    
    