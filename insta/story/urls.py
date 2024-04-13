
from django.urls import path
from . import views

urlpatterns = [
    path('create_story', views.create_story, name='create_story'),
    # path('view_story/<str:username>/', views.view_story, name='view_story'),
    path('view_story/<str:username>/<int:story_id>/', views.view_story, name='view_story'),
    # path('next-story/', views.next_story, name='next-story'),
]





# {% load static %}
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>{{ user.username }}'s Stories</title>
#   <!-- Include Slick Slider CSS -->
#   <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css"/>
#   <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css"/>
# </head>
# <body>
#   <h1>{{ user.username }}'s Stories</h1>
  
#   <div class="slider" data-fetch-next-url="{% url 'next-story' %}">
#     {% for story in stories %}
#       <div>
#         <img src="{{ story.content.url }}" alt="Story Image">
#         <!-- Display other story details as needed -->
#       </div>
#     {% endfor %}
#   </div>

#   <!-- Include jQuery and Slick Slider JS -->
#   <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
#   <script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>



#   <script>
#     $(document).ready(function(){
#       // Initialize Slick Slider
#       var slider = $('.slider').slick({
#         infinite: true,
#         slidesToShow: 1,
#         slidesToScroll: 1,
#         autoplay: false, // Disable autoplay initially
#         dots: true
#       });
  
#       // Add event listener for after slide change
#       slider.on('afterChange', function(event, slick, currentSlide){
#         // Check if it's the last slide
#         console.log(currentSlide)
#         if (currentSlide === slick.$slides.length - 1) {
#           // Fetch and display the next story
#           fetchNextStory();
#         }
#       });
  
#       // Function to fetch and display the next story
#       function fetchNextStory() {
#         // Make an AJAX request to fetch the next story
#         $.ajax({
#           url: 'next-story/',  // Replace with the URL of your fetch-next-story view
#           method: 'GET',
#           success: function(data) {
#             // Append the next story to the slider
#             console.log(data)
#             $('.slider').slick('slickAdd', '<div><img src="' + data.content_url + '" alt="Story Image"></div>');
#           },
#           error: function(xhr, status, error) {
#             console.error('Error fetching next story:', error);
#           }
#         });
#       }
#     });
#   </script>
  
# </body>
# </html>

