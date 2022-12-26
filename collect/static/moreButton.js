const addBtn = document.querySelector(".add");

const input = document.querySelector(".inp-group");

function removeInput() {
    this.parentElement.remove();
}

function addInput() {
    var element = document.getElementsByClassName('inp-group');
    var count = element[0].childElementCount;

    const num = document.createElement("label");
    num.id = String(count + 1)
    num.textContent = String(count + 1).concat(". ")
    num.name = "label"

    const name = document.createElement("input");
    name.type = "text";
    name.id = "symbol".concat(parseInt(count + 1))
    name.placeholder = "Enter a stock";

    const btn = document.createElement("a");
    btn.className = "delete";
    btn.innerHTML = "&times";

    btn.addEventListener("click", removeInput);

    const flex = document.createElement("div");
    flex.className = "form-group";

    input.appendChild(flex);
    flex.appendChild(num)
    flex.appendChild(name);
    flex.appendChild(btn);
}



addBtn.addEventListener("click", addInput);