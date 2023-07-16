$('#toggle > span').click(function () {
    var ix = $(this).index();

    $('#main_table').toggle(ix === 0);
    $('#hidden_table').toggle(ix === 1);
    $('#hidden_table2').toggle(ix === 2);
    $('#hidden_table3').toggle(ix === 3);
});