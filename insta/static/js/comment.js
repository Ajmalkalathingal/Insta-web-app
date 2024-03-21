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
    let form = thisButton.closest('form'); // Find the parent form
    console.log(form)

    $.ajax({
        data: form.serialize(), // Serialize the form data
        method: form.attr('method'), // Use the form's method attribute
        url: form.attr('action'), // Use the form's action attribute
        dataType: 'json',
        success: function (response) {
            console.log(response.data);
            // Append the new comme~nt to the #comments h5 tag
            $('.comments_'+ comment_id).append('<p>' + response.data.comment +' <img src="' + response.data.user.profile_picture + '" alt="User Profile Picture"> </p> ');
            $('#comment_data').val("")
            // Additional handling or DOM updates can be added here
        },
        error: function (error) {
            console.log(error);
        }
    });
});
});