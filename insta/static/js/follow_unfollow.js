// function followUnfollow() {
//     var userId = document.querySelector('.follow-unfollow-btn').dataset.userId;

//     console.log(userId)


//     fetch(`/follow_unfollow/${userId}/`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.is_following) {
//                 console.log(data.is_following)
//                 document.querySelector('.follow-unfollow-btn').innerText = 'Unfollow';
//             } else {
//             console.log(data.is_following)
//                 document.querySelector('.follow-unfollow-btn').innerText = 'Follow';
//             }

//             // Update follower and following counts
//             document.querySelector('.followers-count').innerText = ` Followers - ${data.followers_count}`;
//             document.querySelector('.following-count').innerText = `following - ${data.following_count}`;
//         })
        
//         .catch(error => {
//             console.error('Error:', error);
//         });
// }


// follow_unfollow.js

// Function to get CSRF cookie value
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function followUnfollow(button) {
    var user_id = button.getAttribute('data-user-id');
    console.log('clicked')
    console.log(user_id);


    $.ajax({
        url: `/follow_unfollow/${user_id}/`,
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data) {
            console.log('Follow/Unfollow data:', data);
            var follow_status = data.is_following;
            // Update button text and action based on response
            if (follow_status) {
                console.log(data.is_following)
                button.textContent = 'unfollow';
            } else {
                console.log(data.is_following)
                button.textContent = 'follow';
            }


            // Update follower and following counts
            $('.followers-count').text('Followers ' + data.followers_count);
            $('.following-count').text('Following - ' + data.following_count);

            // Use follow_status value for other purposes if needed
            console.log('Follow Status:', follow_status);
        },
        error: function (error) {
            console.log(error);
        }
    });
}
