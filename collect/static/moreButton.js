const addBtn = document.querySelector(".add");


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



addBtn.addEventListener("click", addInput);