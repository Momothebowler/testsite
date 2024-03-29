var width = 1
$('#post-form').submit(function (e) {
    e.preventDefault();
    document.getElementById("table-btn").style.display = "none";
    document.getElementById("myProgress").style.display = "block";
    data = {};
    data['iters'] = $('#Iterations').val();
    max = data['iters'];
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
            $("div[name='Table1']").html("");
            $("div[name='Table1']").html(data_obj.df);
            $("div[name='Table2']").html("");
            $("div[name='Table2']").html(data_obj.df2);
            document.getElementById("table-btn").style.display = "";
            document.getElementById("myProgress").style.display = "none";
            width = 101;   
        }
    });
});


function move() {
  var elem = document.getElementById("myBar");   
  width = 1;
  var max = $('#Iterations').val();
  var id = setInterval(frame, max * 10);
  function frame() {
    if (width >= 100) {
      clearInterval(id);
      elem.style.width = 0 + '%';
    } else {
      width++; 
      elem.style.width = width + '%'; 
    }
  }
}