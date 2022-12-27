$(document).on('submit', '#post-form', function (e) {
    document.getElementById("create-btn").style.display = "none";
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'create',
        data: {
            name: $('#name').text(),
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            $('#name').html(data);
            console.log($("#create-btn"))
        }
    });
});