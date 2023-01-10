$('#post-form').submit(function (e) {
    e.preventDefault();
    document.getElementById("table-btn").style.display = "none";
    document.getElementById("myProgress").style.display = "block";
    data = {};
    data['iters'] = $('#Iterations').val();
    data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();
    var count1 = document.querySelector('form .step-1').querySelector(".inp-group").childElementCount;
    data['count1'] = count1
    for (let x = 1; x <= count1; x++) {
        data['symbol'.concat(parseInt(x))] = $('#symbol'.concat(parseInt(x))).val();
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
            document.getElementById("table-btn").style.display = "";
            document.getElementById("myProgress").style.display = "none";
            document.getElementById("myBar").style.width = 0 + '%';
        }
    });
});

var i = 0;
function move() {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 200);
    function frame() {
      if (width >= 100) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
      }
    }
  }
}