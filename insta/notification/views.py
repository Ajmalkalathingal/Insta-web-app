from django.shortcuts import render,redirect,get_object_or_404
from . models import Notification

# Create your views here.
def notification_view(request):
    user = request.user
    notification = Notification.objects.filter(user=user).order_by('-date')
    notification.update(is_read=True)

    context = {
        'notifications':notification
    }
    return render(request, 'notification.html', context)


def del_notification(request, id):
    # Retrieve the notification with the given ID
    notification = get_object_or_404(Notification, id=id, user=request.user)
    print(notification)
    get_object_or_404(Notification, id=id, user=request.user).delete()

    # Redirect back to the notification page
    return redirect(notification_view)