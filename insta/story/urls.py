
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('create_story', views.create_story, name='create_story'),
    # path('view_story/<str:username>/', views.view_story, name='view_story'),
    path('view_story/<str:username>/<int:story_id>/', views.view_story, name='view_story'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()