from django.db import models
from django.contrib.auth.models import User



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sent_messages')
    receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,related_name='received_messages')
    message = models.TextField(null=True, blank=True)
    theard_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='messaged_image',null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)    

    def __str__(self) -> str:
        return f"{self.message or self.image}"
    

class Notificaton(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_notification')
    receiver = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,related_name='receiver_notification')
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE,null=True)
    is_seen = models.BooleanField(default=False) 


    
    