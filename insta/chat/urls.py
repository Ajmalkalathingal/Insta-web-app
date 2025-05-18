from django.urls import path 
from . import views

urlpatterns = [
    path('<int:user_id>/', views.main_chat, name='main_chat'),
    path('chat/<str:group_name>/', views.main_chat, name='group_chat'),
    path('chat/', views.chat, name='chat'),
    path('load-users/', views.load_users, name='load_users'),
]





# {% extends 'base.html' %}
# {% load static %}
# {% block content %}

# <link rel="stylesheet" href="{% static 'assets3/css/chat_list.css' %}" />

# <div class="main-wrapper mt-5">
#   <div class="container">
#     <div class="page-content">
#       <div class="row">
#         <div class="col-md-10 col-12 card-stacked">
#           <div class="card shadow-line mb-3 chat chat-panel">
#             <!-- Chat Header -->
#             <div class="p-3 chat-header">
#               <div class="d-flex">
#                 <div class="w-100 d-flex pl-0">
#                   {% if chat_type == 'group' %}
#                     <img class="rounded-circle shadow avatar-sm mr-3 chat-profile-picture"
#                          src="{{ group.image.url|default:'https://via.placeholder.com/40' }}" alt="{{ group.name }}">
#                     <div class="mr-3">
#                       <p class="fw-400 mb-0 text-dark-75">{{ group.name }}</p>
#                       <p class="sub-caption text-muted text-small mb-0">
#                         Group Chat
#                       </p>
#                     </div>
#                   {% else %}
#                     {% if receiver_user.profile.image %}
#                       <img class="rounded-circle shadow avatar-sm mr-3 chat-profile-picture"
#                            src="{{ receiver_user.profile.image.url }}" alt="{{ receiver_user.username }}">
#                     {% else %}
#                       <img class="rounded-circle shadow avatar-sm mr-3 chat-profile-picture"
#                            src="https://user-images.githubusercontent.com/35243461/168796877-f6c8819a-5d6e-4b2a-bd56-04963639239b.jpg"
#                            alt="default avatar">
#                     {% endif %}
#                     <div class="mr-3">
#                       <p class="fw-400 mb-0 text-dark-75">{{ receiver_user.username }}</p>
#                       <p class="sub-caption text-muted text-small mb-0">
#                         {% if last_seen %}
#                           Last seen {{ last_seen|date:"M d, Y" }} at {{ last_seen|date:"h:i A" }}
#                         {% else %}
#                           No activity
#                         {% endif %}
#                       </p>
#                     </div>
#                   {% endif %}
#                 </div>
#               </div>
#             </div>

#             <!-- Chat Messages -->
#             <div class="d-flex flex-row mb-3 navigation-mobile scrollable-chat-panel chat-panel-scroll">
#               <div class="w-100 p-3">
#                 <div class="chat-messages scrollable-chat-panel">
#                   <div class="text-center letter-space drop-shadow text-uppercase fs-12 w-100 mb-3">Today</div>

#                   {% for message in messages %}
#                     {% if message.user == request.user %}
#                       <!-- Sent Message -->
#                       <div class="d-flex flex-row-reverse mb-2">
#                         <div class="right-chat-message fs-13 mb-2">
#                           <div class="mb-0 mr-3 pr-4">
#                             <div class="d-flex flex-row">
#                               {% if message.image %}
#                                 <img src="{{ message.image.url }}" alt="Message Image" class="chat-message-image">
#                               {% else %}
#                                 <p class="mb-0 mr-3 pr-4">{{ message.message }}</p>
#                               {% endif %}
#                             </div>
#                           </div>
#                           <div class="message-options dark">
#                             <div class="message-time d-flex flex-row">
#                               <div class="mr-2">{{ message.date|time:"H:i" }}</div>
#                               {% if message.is_read %}
#                                 <div class="svg15 double-check"></div>
#                               {% endif %}
#                             </div>
#                           </div>
#                         </div>
#                       </div>
#                     {% else %}
#                       <!-- Received Message -->
#                       <div class="left-chat-message fs-13 mb-2">
#                         {% if chat_type == "group" %}
#                           <strong class="d-block">{{ message.user.username }}</strong>
#                         {% endif %}
#                         {% if message.image %}
#                           <img src="{{ message.image.url }}" alt="Message Image" class="chat-message-image">
#                         {% else %}
#                           <p class="mb-0 mr-3 pr-4">{{ message.message }}</p>
#                         {% endif %}
#                         <div class="message-options">
#                           <div class="message-time">{{ message.date|time:"H:i" }}</div>
#                         </div>
#                       </div>
#                     {% endif %}
#                   {% empty %}
#                     <p class="text-muted text-center">No messages yet.</p>
#                   {% endfor %}
#                 </div>
#               </div>
#             </div>

#             <!-- Chat Input -->
#             <div class="chat-input fixed-input-area">
#               <div class="chat-search pl-3 pr-3">
#                 <div class="input-group">
#                   <input type="text" class="form-control" placeholder="Write a message">
#                   <div class="input-group-append prepend-white">
#                     <span class="input-group-text pl-2 pr-2">
#                       <i id="chat-upload" class="chat-upload-trigger fs-19 bi bi-file-earmark-plus ml-2 mr-2"></i>
#                       <input type="file" id="chat-file-input" style="display: none;" accept="image/*" />
#                       <i class="fs-19 bi bi-cursor ml-2 mr-2"></i>
#                     </span>
#                   </div>
#                 </div>
#               </div>
#             </div>

#             <!-- Hidden JSON Data -->
#             {{ request.user.id|json_script:"json-current-user-id" }}
#             {% if chat_type == "group" %}
#               {{ group.id|json_script:"json-group-id" }}
#               {{ group.name|json_script:"json-group-name" }}
#             {% else %}
#               {{ receiver_user.id|json_script:"json-receiver-id" }}
#               {{ receiver_user.username|json_script:"json-receiver-username" }}
#             {% endif %}
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
# </div>

# <script src="{% static 'js/chat/message.js' %}"></script>
# {% endblock %}
  
