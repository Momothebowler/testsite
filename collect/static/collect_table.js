var width = 1
$('#post-form').submit(function (e) {
  e.preventDefault();
  document.getElementById("table-btn").style.display = "none";
  document.getElementById("myProgress").style.display = "block";
  data = {};
  data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();
  var count1 = document.querySelector('form .step-1').querySelector(".inp-group").childElementCount;
  data['count1'] = count1
  var count2 = 0;
  for (let x = 1; x <= count1; x++) {
    data['symbol'.concat(parseInt(x))] = $('#symbol'.concat(parseInt(x))).val();
    if ($('#symbol'.concat(parseInt(x))).val()) {
      count2 += 1;
    }
    data['Allocation'.concat(parseInt(x)).concat("_1")] = $('#Allocation'.concat(parseInt(x)).concat("_1")).val();
  }
  data['iters'] = $('#Iterations').val();
  max = data['iters'];
  $.ajax({
    type: 'POST',
    url: 'create',
    data: data,
    success: function (data) {
      var data_obj = JSON.parse(data);
      $("div[name='Table1']").html("");
      $("div[name='Table1']").html(data_obj.df);
      $("div[name='Table2']").html("");
      $("div[name='Table2']").html(data_obj.df2);
      document.getElementById("table-btn").style.display = "";
      document.getElementById("myProgress").style.display = "none";
      width = 101;
      //Count2 gives us the offset
      for (let i = 1; i <= 2; i++) {
        var startBal = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 1).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 1).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(startBal).concat("<span class='tooltiptext'>Initial Balance of Account.</span></div>");
        var endBal = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 2).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 2).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(endBal).concat("<span class='tooltiptext'>End Balance of Account.</span></div>");
        var annualizedReturn = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 3).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 3).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(annualizedReturn).concat("<span class='tooltiptext'>Return expected from a single year.</span></div>");
        var expectedReturn = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 4).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 4).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(expectedReturn).concat("<span class='tooltiptext'>Percentage return expected over a year.</span></div>");

        var std = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 5).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 5).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(std).concat("<span class='tooltiptext'>Standard Deviation.</span></div>");
        var bestYear = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 6).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 6).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(bestYear).concat("<span class='tooltiptext'>Most Money Made In A Single Year.</span></div>");

        var worstYear = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 7).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 7).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(worstYear).concat("<span class='tooltiptext'>Least Money Made/Lost In A Single Year.</span></div>");
        var maxDrawdown = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 8).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 8).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(maxDrawdown).concat("<span class='tooltiptext'>Something something.</span></div>");
        var exAnte = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 9).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 9).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(exAnte).concat("<span class='tooltiptext'>Up the bets.</span></div>");
        var exPost = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 10).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 10).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(exPost).concat("<span class='tooltiptext'>Why did you bet.</span></div>");
        var sortino = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 11).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 11).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(sortino).concat("<span class='tooltiptext'>Special Ratio.</span></div>");
        var stockCorrelation = document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 12).concat(") > td:nth-child(1)"))).innerHTML;
        document.querySelector("#Table".concat(i).concat("> table > tbody > tr:nth-child(".concat(count2 + 12).concat(") > td:nth-child(1)"))).innerHTML = "<div class='tooltip'>".concat(stockCorrelation).concat("<span class='tooltiptext'>How closely follows stock market.</span></div>");
      };

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