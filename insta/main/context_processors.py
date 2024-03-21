from Authuser.models import UserProfile
from notification.models import Notification

def custom_context(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        notification_count = Notification.objects.filter(user=user,is_read=False).count()
        print(notification_count)

        return {
            'user_profile':user_profile,
            'notification_count':notification_count
        }
        
    else:
        return {}