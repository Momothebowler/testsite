$(document).on('submit', '#post-form', function (e) {
    document.getElementById("create-btn").style.display = "none";
    e.preventDefault();
    data = {}
    data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val()
    var element = document.getElementsByClassName('inp-group');
    var count = element[0].childElementCount;
    data['count'] = count
    for (let x = 1; x <= count + 1; x++) {
        data['symbol'.concat(parseInt(x))] = $('#symbol'.concat(parseInt(x))).val()
    }
    $.ajax({
        type: 'POST',
        url: 'create',
        data: data,
        success: function (data) {
            $('#name').html(data);
            console.log($("#create-btn"))
        }
    });
});