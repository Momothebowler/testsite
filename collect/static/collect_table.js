$('#post-form').submit(function (e) {
    e.preventDefault();
    document.getElementById("table-btn").style.display = "none";
    data = {};
    data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();
    var count1 = document.querySelector('form .step-1').querySelector(".inp-group").childElementCount;
    var count2 = document.querySelector('form .step-2').querySelector(".inp-group").childElementCount;
    var count3 = document.querySelector('form .step-3').querySelector(".inp-group").childElementCount;
    data['count1'] = count1
    data['count2'] = count2
    data['count3'] = count3
    for (let x = 1; x <= count1; x++) {
        data['symbol'.concat(parseInt(x))] = $('#symbol'.concat(parseInt(x))).val();
    }
    for (let x = 1; x <= count2; x++) {
        data['Allocation'.concat(parseInt(x)).concat("_1")] = $('#Allocation'.concat(parseInt(x)).concat("_1")).val();
    }
    $.ajax({
        type: 'POST',
        url: 'create',
        data: data,
        success: function (data) {
            var data_obj = JSON.parse(data)
            $("div[name='name']").html("");
            $("div[name='name']").html(data_obj.df);
            $('#notice').html('<h3>'.concat(data_obj.message[0]).concat('</h3>'));
            document.getElementById("table-btn").style.display = "";
        }
    });
});