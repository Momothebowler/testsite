function tableCreate(title, stocks, bonds, currency) {
    rows = Math.max(stocks.length, bonds.length, currency.length);
    const table_div = document.getElementById("main_table"),
        tbl = document.createElement('table');
    tbl.setAttribute("style", "width:100%");
    var boxes = 0;
    for (let i = 0; i < rows + 1; i++) { // +1 for title
        const tr = tbl.insertRow();
        for (let j = 0; j < title.length; j++) {
            if (i > 0) {
                var words = "";
                var blank = true;
                var td = tr.insertCell();
                switch (j) {
                    case 0:
                        words = stocks[i - 1];
                        blank = false;
                        break;
                    case 1:
                        if (i <= stocks.length) {
                            td.setAttribute("id", "stock_" + (i - 1));
                        }
                        blank = false;
                        break;
                    case 2:
                        var wrapper = document.createElement("div");
                        wrapper.setAttribute("class", "checkbox-wrapper-1");
                        wrapper.setAttribute("id", "stock_wrapper_" + (i - 1));
                        var wrapper_input = document.createElement("input");
                        wrapper_input.setAttribute("class", "substituted");
                        wrapper_input.setAttribute("id", ("example-" + boxes));
                        wrapper_input.setAttribute("type", "checkbox");
                        wrapper_input.setAttribute("aria-hidden", "true");
                        var wrapper_label = document.createElement("label");
                        wrapper_label.setAttribute("for", ("example-" + boxes));
                        boxes += 1;
                        blank = true;
                        break;
                    case 3:
                        words = bonds[i - 1];
                        blank = false;
                        break;
                    case 4:
                        if (i <= bonds.length) {
                            td.setAttribute("id", "bond_" + (i - 1))
                        }
                        blank = false;
                        break;
                    case 5:
                        words = undefined;
                        var wrapper = document.createElement("div");
                        wrapper.setAttribute("class", "checkbox-wrapper-1");
                        wrapper.setAttribute("id", "bond_wrapper_" + (i - 1));
                        var wrapper_input = document.createElement("input");
                        wrapper_input.setAttribute("class", "substituted");
                        wrapper_input.setAttribute("id", ("example-" + boxes));
                        wrapper_input.setAttribute("type", "checkbox");
                        wrapper_input.setAttribute("aria-hidden", "true");
                        var wrapper_label = document.createElement("label");
                        wrapper_label.setAttribute("for", ("example-" + boxes));
                        boxes += 1;
                        blank = true;
                        break;
                    case 6:
                        words = currency[i - 1];
                        blank = false;
                        break;
                    case 7:
                        if (i <= currency.length) {
                            td.setAttribute("id", "currency_" + (i - 1))
                        }
                        blank = false;
                        break;
                    case 8:
                        blank = false;
                        break;
                }
                if (blank === false) {
                    if (words === undefined) {
                        words = "";
                    }
                    td.appendChild(document.createTextNode(words));
                } else {
                    td.appendChild(document.createTextNode(""));
                    td.appendChild(wrapper);
                    wrapper.appendChild(wrapper_input);
                    wrapper.appendChild(wrapper_label);
                }
            } else {
                var td = tr.insertCell();
                td.setAttribute("style", "font-weight: bold;text-align: center;")
                td.appendChild(document.createTextNode(title[j]));
            }
        }
    }
    table_div.appendChild(tbl);
}

const title = ["Stocks", "", "lock", "Bonds", "", "lock", "Currency", "", "lock"]; //Leave as is
const stocks = ["AMD", "BBBY", "COF", "DE", "SPY", "QQQ"];
const stock_weights = [40, 20, 20, 15, 5];
const bonds = ["BAC", "BND", "CWB", "DFSD", "AAPL", "TQQQ", "SQQQ"];
const bond_weights = [40, 30, 20, 10];
const currency = ["BTC", "ETH"];
const currency_weights = [75, 25];
tableCreate(title, stocks, bonds, currency);

var slider1 = document.getElementById("myRange1");
var output1 = document.getElementById("demo1");
var slider2 = document.getElementById("myRange2");
var output2 = document.getElementById("demo2");
var slider3 = document.getElementById("myRange3");
var output3 = document.getElementById("demo3");
var labelA = document.getElementById("A");
var labelB = document.getElementById("B");
var labelC = document.getElementById("C");
var labelD = document.getElementById("D");
output1.innerHTML = slider1.value;
output2.innerHTML = slider2.value;
output3.innerHTML = slider3.value;
var stock_value = ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 10000 * 100;
var bond_value = (100 - ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 100);
var currency_value = 0;
updateTable(stock_weights, bond_weights, currency_weights, stock_value, bond_value, currency_value, stocks, bonds, currency)

slider1.oninput = function () {
    output1.innerHTML = this.value;
    stock_value = ((this.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 10000 * 100;
    bond_value = (100 - ((this.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 100);
    updateTable(stock_weights, bond_weights, currency_weights, stock_value, bond_value, currency_value, stocks, bonds, currency)
}

slider2.oninput = function () {
    output2.innerHTML = this.value;
    stock_value = ((slider1.value * 20) + (this.value * 70) + (slider3.value * 10)) / 10000 * 100;
    bond_value = (100 - ((slider1.value * 20) + (this.value * 70) + (slider3.value * 10)) / 100);
    updateTable(stock_weights, bond_weights, currency_weights, stock_value, bond_value, currency_value, stocks, bonds, currency)
}

slider3.oninput = function () {
    output3.innerHTML = this.value;
    stock_value = ((slider1.value * 20) + (slider2.value * 70) + (this.value * 10)) / 10000 * 100;
    bond_value = (100 - ((slider1.value * 20) + (slider2.value * 70) + (this.value * 10)) / 100);
    updateTable(stock_weights, bond_weights, currency_weights, stock_value, bond_value, currency_value, stocks, bonds, currency)
}

function updateTable(stock_weights, bond_weights, currency_weights, stock_value, bond_value, currency_value, stocks, bonds, currency) {
    //can tell if checked by getting object and putting .checked
    for (let i = 0; i < stocks.length; i++) {
        stock_percent = document.getElementById("stock_" + i);
        if (document.getElementById("example-" + (i * 2)).checked === false) {
            stock_percent.textContent = (Math.round(stock_weights[i] * stock_value) / 100).toFixed(2) + "%";
        }

    }
    for (let i = 0; i < bonds.length; i++) {
        bond_percent = document.getElementById("bond_" + i);
        if (document.getElementById("example-" + (i * 2 + 1)).checked === false) {
            bond_percent.textContent = (Math.round(bond_weights[i] * bond_value) / 100).toFixed(2) + "%";
        }

    }

    for (let i = 0; i < currency.length; i++) {
        //currency_percent = document.getElementById("currency_" + i);
        //currency_percent.textContent = (Math.round(currency_weights[i] * 5000) / 100).toFixed(2) + "%"; // currency_value)/100+"%";
    }


}

$('.upload_table > span').click(function () {
    var ix = $(this).index();
    if (ix === 0) {
        slider1.value = 30;
        slider2.value = 50;
        slider3.value = 90;

        stock_value = ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 10000 * 100;
        bond_value = (100 - ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 100);

        for (let i = 0; i < stocks.length; i++) {
            stock_percent = document.getElementById("stock_" + i);

            if (document.getElementById("example-" + (i * 2)).checked === false) {
                stock_percent.textContent = (Math.round(stock_weights[i] * stock_value) / 100).toFixed(2) + "%";
            }

        }
        for (let i = 0; i < bonds.length; i++) {
            bond_percent = document.getElementById("bond_" + i);
            if (document.getElementById("example-" + (i * 2 + 1)).checked === false) {
                bond_percent.textContent = (Math.round(bond_weights[i] * bond_value) / 100).toFixed(2) + "%";
            }

        }

        for (let i = 0; i < currency.length; i++) {
            //currency_percent = document.getElementById("currency_" + i);
            //currency_percent.textContent = (Math.round(currency_weights[i] * 5000) / 100).toFixed(2) + "%"; // currency_value)/100+"%";
        }
        $('#main_table').toggle();
        $('#hidden_table').toggle();
    }
    if (ix === 1) {
        slider1.value = 30;
        slider2.value = 50;
        slider3.value = 90;
        slider1.value = 90;
        slider2.value = 20;
        slider3.value = 45;

        stock_value = ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 10000 * 100;
        bond_value = (100 - ((slider1.value * 20) + (slider2.value * 70) + (slider3.value * 10)) / 100);

        for (let i = 0; i < stocks.length; i++) {
            stock_percent = document.getElementById("stock_" + i);
            if (document.getElementById("example-" + (i * 2)).checked === false) {
                stock_percent.textContent = (Math.round(stock_weights[i] * stock_value) / 100).toFixed(2) + "%";
            }

        }
        for (let i = 0; i < bonds.length; i++) {
            bond_percent = document.getElementById("bond_" + i);
            if (document.getElementById("example-" + (i * 2 + 1)).checked === false) {
                bond_percent.textContent = (Math.round(bond_weights[i] * bond_value) / 100).toFixed(2) + "%";
            }

        }

        for (let i = 0; i < currency.length; i++) {
            //currency_percent = document.getElementById("currency_" + i);
            //currency_percent.textContent = (Math.round(currency_weights[i] * 5000) / 100).toFixed(2) + "%"; // currency_value)/100+"%";
        }
        $('#main_table').toggle();
        $('#hidden_table').toggle();
    }
});