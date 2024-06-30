
window.onload = function() {
// Get the order description from localStorage
const orderDescription = JSON.parse(localStorage.getItem('orderDescription')) || [];

// Calculate subtotal
let subtotal = 0;
orderDescription.forEach(item => {
subtotal += item['item-quantity'] * item['item-price'];
});

// Update subtotal in order summary
const subtotalElement = document.querySelector('.all-item-subtotal');
subtotalElement.textContent = `$${subtotal.toFixed(2)}`;

// Placeholder for tax and shipping
const taxElement = document.querySelector('.items-tax');
taxElement.textContent = '$5';

const shippingElement = document.querySelector('.item-shipping');
shippingElement.textContent = '$10';

// Calculate total
const total = subtotal + 5 + 10;

// Update total in order summary
const totalElement = document.querySelector('.item-total');
totalElement.textContent = `$${total.toFixed(2)}`;

// Use the order description to populate the order details
orderDescription.forEach(item => {
const orderItem = document.createElement('div');
orderItem.classList.add('order-item');

const quantityElement = document.createElement('span');
quantityElement.classList.add('item-quantity');
quantityElement.textContent = item['item-quantity'] + 'x'; // Add 'x' after quantity
orderItem.appendChild(quantityElement);

const imageElement = document.createElement('img');
imageElement.src = item['item-image'];
imageElement.style.width = '50px';  // Set the width as needed
imageElement.style.height = '50px';  // Set the height as needed
orderItem.appendChild(imageElement);

const descriptionText = document.createElement('span');
descriptionText.classList.add('item-description');

const nameElement = document.createElement('span');
nameElement.classList.add('item-name');
nameElement.textContent = item['item-name'];
descriptionText.appendChild(nameElement);

const sizeElement = document.createElement('span');
sizeElement.classList.add('item-size');
sizeElement.textContent = ' - Size ' + item['item-size']; // Add size
descriptionText.appendChild(sizeElement);

const priceElement = document.createElement('span');
priceElement.classList.add('item-price');
priceElement.textContent = ' - $' + item['item-price']; // Add price
descriptionText.appendChild(priceElement);

orderItem.appendChild(descriptionText);

document.querySelector('.details').appendChild(orderItem);
});
};

function closeContainer() {
// Clear order details from localStorage
localStorage.removeItem('orderDescription');

// Redirect to cart.html
window.location.href = '{% url "web:cart" %}';
}

document.addEventListener('DOMContentLoaded', function() {
const payNowButton = document.querySelector('button');
const successPopup = document.getElementById('successPopup');

// JavaScript code for form validation and other functions

function validateForm(event, formId) {
event.preventDefault(); // Prevent form submission
const form = document.getElementById(formId);
const errorPopup = document.getElementById('errorPopup');

// Check if all required inputs in the form are filled
const isValid = Array.from(form.elements).every(element => {
    return !element.required || (element.required && element.value.trim() !== '');
});

if (isValid) {
    // If the form is valid, submit it
    form.submit();
} else {
    // If the form is not valid, display the error pop-up
    errorPopup.style.display = 'block';
}
}
if (payNowButton) {
payNowButton.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default form submission
  
  // Remove items from the cart
  localStorage.removeItem('cart');
  
  // Show success popup
  successPopup.style.display = 'block';
  
  // Hide success popup after 3 seconds (3000 milliseconds)
  setTimeout(function() {
    successPopup.style.display = 'none';
  }, 3000);
});
}
});

document.addEventListener('DOMContentLoaded', function() {
// Retrieve order description from localStorage
const orderDescription = JSON.parse(localStorage.getItem('orderDescription')) || [];

// Populate hidden input fields with item details
orderDescription.forEach(function(item, index) {
    document.getElementById('item_name_' + index).value = item['item-name'];
    document.getElementById('item_price_' + index).value = item['item-price'];
    document.getElementById('item_size_' + index).value = item['item-size'];
    document.getElementById('item_quantity_' + index).value = item['item-quantity'];
});
});
