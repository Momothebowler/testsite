const steps = Array.from(document.querySelectorAll('form .step'));
const form = document.querySelector('form');

function changeStep(btn) {
    let index = 0;
    const active = document.querySelector('form .step.active');
    index = steps.indexOf(active);
    steps[index].classList.remove('active');
    if (btn === 'next') {
        index++;
    } else if (btn === 'prev') {
        index--;
    }
    steps[index].classList.add('active')
}

function addRow(ele) {
    console.log(typeof ele.id)
    str = ele.id
    num = parseInt(str.split("n")[1].split("_")[0], 10);
    console.log(num)
    console.log("hhhhhhhhh")
    var element = document.querySelector('form .step.active').querySelector(".inp-group")
    var count = element.childElementCount;
    if (num == count - 1) {
        var index_string = document.querySelector('form .step.active').className.split(" ")[1]

        const nums = document.createElement("label");
        nums.id = String(count + 1)
        nums.textContent = String(count + 1).concat(". ")
        nums.name = "label"

        const name = document.createElement("input");
        name.type = "text";
        name.disabled = true;
        if (index_string === "step-1") {
            name.id = "symbol".concat(parseInt(count + 1))
            name.placeholder = "Enter a stock";
        }

        const name2 = document.createElement("input");
        name.type = "text";
        name2.disabled = true;
        if (index_string === "step-1") {
            name2.id = "Allocation".concat(parseInt(count + 1)).concat("_1")
            name2.placeholder = "Stock ".concat(String(count + 1)).concat(" Allocation");
        }

        const btn = document.createElement("a");
        btn.className = "delete";
        btn.innerHTML = "&times";

        btn.addEventListener("click", removeInput);

        const flex = document.createElement("div");
        flex.className = "form-group";

        element.appendChild(flex);
        flex.appendChild(nums)
        flex.appendChild(name);
        flex.appendChild(name2);
        flex.appendChild(btn);


    }
    ele.setAttribute("onkeyup", "");
    document.querySelector("#symbol".concat(String(num + 1))).disabled = false;
    document.querySelector("#table-btn").disabled = false;
    document.querySelector("#Allocation".concat(String(num + 1).concat("_1"))).disabled = false;
    document.querySelector("#Allocation".concat(String(num + 1).concat("_1"))).setAttribute("onkeyup", "addRow(this)");

    //inputs[i].disabled=true;
}

function removeInput() {
    this.parentElement.remove();
}

function addInput() {
    var element = document.querySelector('form .step.active').querySelector(".inp-group")
    var count = element.childElementCount;
    var index_string = document.querySelector('form .step.active').className.split(" ")[1]

    const num = document.createElement("label");
    num.id = String(count + 1)
    num.textContent = String(count + 1).concat(". ")
    num.name = "label"

    const name = document.createElement("input");
    name.type = "text";
    if (index_string === "step-1") {
        name.id = "symbol".concat(parseInt(count + 1))
        name.placeholder = "Enter a stock";
    }

    const name2 = document.createElement("input");
    name.type = "text";
    if (index_string === "step-1") {
        name2.id = "Allocation".concat(parseInt(count + 1)).concat("_1")
        name2.placeholder = "Stock ".concat(String(count + 1)).concat(" Allocation");
        name2.type = "number"
        name2.min = "0"
        name2.max = "100"
    }

    const btn = document.createElement("a");
    btn.className = "delete";
    btn.innerHTML = "&times";

    btn.addEventListener("click", removeInput);

    const flex = document.createElement("div");
    flex.className = "form-group";

    element.appendChild(flex);
    flex.appendChild(num)
    flex.appendChild(name);
    flex.appendChild(name2);
    flex.appendChild(btn);
}



