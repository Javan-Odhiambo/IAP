var sizeButtons = document.querySelectorAll('.size-btns');
var currSize=document.querySelector('.size-value')

for (var i = 0; i < sizeButtons.length; i++) {
  var button = sizeButtons[i];
  button.addEventListener('click', function (event) {
    getSize(event);
  });
}
function getSize(event) {
  var button = event.target;
  var size = button.innerText; 
  
  currSize.innerText=size
}

var colorButtons =document.querySelectorAll('.color-btns');
var currentColor=document.querySelector('.color-value')
for(var i=0;i<colorButtons.length;i++){
  var colorButton=colorButtons[i]
  colorButton.addEventListener('click',function(event){
    getColor(event);
  });
}
function getColor(event){
  var colorButton=event.target;
  var color=colorButton.innerText;
  currentColor.innerText=color
}


var quantityBtns = document.querySelectorAll('.quantity-btns');
var quantitySelect = document.querySelector('.quantity-value');
var quantity = parseFloat(quantitySelect.innerText);
var priceSelector = document.querySelector('.price-value');
var price = parseFloat(priceSelector.innerText);
var subtotalSelector = document.querySelector('.sub-value');
var subtotal = calculateSubtotal(quantity, price);
subtotalSelector.innerText = subtotal;


for (var i = 0; i < quantityBtns.length; i++) {
  var quantityButton = quantityBtns[i];
  quantityButton.addEventListener('click', function (event) {
    updateQuantityAndSubtotal(event);
  });
}

function updateQuantityAndSubtotal(event) {
  var quantityButton = event.target;
  var operand = quantityButton.innerText;

  if (operand === '-' && quantity > 0) {
    quantity -= 1;
  } else {
    quantity += 1;
  }

  subtotal = calculateSubtotal(quantity, price);
  quantitySelect.innerText = quantity;
  subtotalSelector.innerText = subtotal;
}

function calculateSubtotal(quantity, price) {
  return quantity * price;
}

