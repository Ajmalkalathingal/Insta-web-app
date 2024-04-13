function toggleCommentBox(id) {
    var commentBox = document.querySelector('#comment-box_'+id);
    commentBox.style.display = (commentBox.style.display === 'none' || commentBox.style.display === '') ? 'block' : 'none';
}


$(document).ready(function () {
    $('.submit-comment').on('click', function (e) {
    e.preventDefault(); 

    let thisButton = $(this);
    let comment_id = thisButton.attr('data-comment-id');
    console.log(comment_id)
    let form = thisButton.closest('form'); 
    console.log(form)

    $.ajax({
        data: form.serialize(), // Serialize the form data
        method: form.attr('method'), // Use the form's method attribute
        url: form.attr('action'), // Use the form's action attribute
        dataType: 'json',
        success: function (response) {
            console.log(response.data);
            // Append the new comment to the appropriate container
            var newComment = '<div class="comment d-flex align-items-start pb-2">' +
                '<img src="' + response.data.user.profile_picture + '" alt="' + response.data.user.username + ' Profile Picture" class="me-2" style="border-radius: 50%;" width="30px" height="30px">' +
                '<div class="comment-content">' +
                '<small class="small fs-6">' + response.data.user.username + '</small>' +
                '<p class="container mt-2" style="font-size: 13px;">' + response.data.comment + '</p>' +
                '</div>' +
                '</div>';
    
            $('.comments_'+ comment_id).append(newComment);
            $('.comment_data').val(""); // Clear the comment input field
            
        },
        error: function (error) {
            console.log(error);
        }
    });
    
});
});
