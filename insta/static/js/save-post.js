
// $(document).ready(function () {
//     $('.save_post').click(function (e) {
//         e.preventDefault();

//         let this_val = $(this);
//         let save_post_id = this_val.attr('data-postsave-id');

//         console.log(save_post_id, 'post_id');

//         $.ajax({
//             url: `/save_post/${save_post_id}/`,
//             type: 'POST',
//             dataType: 'json',
//             success: function (data) {
//                 console.log('data', data);
//             },
//             error: function (error) {
//                 console.log(error);
//             }
//         });
//     });

// });

$(document).ready(function () {

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

    $('.save_post').click(function (e) {
        e.preventDefault();

        let save_post_id = $(this).attr('data-postsave-id');
        let icon = $(this);

        console.log(save_post_id, 'post_id');

        $.ajax({
            url: `/save-post/${save_post_id}/`,
            type: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function (data) {
                console.log('data', data);
                // Check if the post is saved
                if (data.message == 'Post saved successfully.') {
                    // If saved, change the icon to a filled bookmark
                    icon.removeClass('fa-regular fa-bookmark').addClass('fa-solid fs-5 fa-bookmark');
                } else {
                    // If not saved, keep the icon as it is
                    icon.removeClass('fa-solid fa-bookmark').addClass('fa-regular fs-5 fa-bookmark');
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
