// like post 
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

    $('.toggle-like').click(function (e) {
    e.preventDefault();

    let this_val = $(this);
    let post_id = this_val.attr('data-post-id');
    let like_count = $('#like_' + post_id); 

    console.log(post_id, 'post_id');
    // console.log(like_count,'count');

    $.ajax({
        url: `/toggle-like/${post_id}/`,
        type: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data) {
            console.log('data', data);
            if (data.liked) {
                // User liked the post
                $(like_count).text(data.count + ' likes');
                $(post_id).css('color', 'red')
            } else {
                // User unliked the post
                $(like_count).text(data.count + ' likes');
                $(post_id).css('background', 'none')
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
});

});