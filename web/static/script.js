document.addEventListener('DOMContentLoaded', (event) => {
  const bar = document.getElementById('bar');
  const nav = document.getElementById('navbar');
  const close = document.getElementById('close');
  const cartCountElement = document.querySelector('.icon-cart span');

  if (bar) {
    bar.addEventListener('click', () => {
      nav.classList.add('active');
    });
  }

  if (close) {
    close.addEventListener('click', () => {
      nav.classList.remove('active');
    });
  }

  // Cart Working js

  if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
  } else {
    ready();
  }

  // Making Function

  function ready() {
    // Remove Items From Cart
    document.addEventListener('click', function (event) {
      if (event.target && event.target.classList.contains('cart-remove')) {
        removeCartItem(event);
      }
    });

    // Quantity Changes
    const quantityInputs = document.getElementsByClassName('cart-quantity');
    for (let i = 0; i < quantityInputs.length; i++) {
      const input = quantityInputs[i];
      input.addEventListener('change', quantityChanged);
    }
  }

// Function to update cart count
function updateCartCount() {
  const cartCountElement = document.querySelector('.icon-cart span');
  const cartData = JSON.parse(localStorage.getItem('cart')) || [];
  const uniqueItems = new Set(cartData.map(item => item.name)); // Using a Set to count unique items
  let totalCount = 0;
  uniqueItems.forEach(itemName => {
    totalCount += 1; // Counting each unique item only once
  });
  cartCountElement.textContent = totalCount;
}

// Call the updateCartCount function when the page loads
document.addEventListener('DOMContentLoaded', function () {
  updateCartCount();
});

  // Function to update cart subtotal and full cart
  function updateCartTotals() {
    let subtotal = 0;
    $('.cart-total-price').each(function () {
      subtotal += parseFloat($(this).text().replace('$', ''));
    });

    // Update the cart subtotal
    $('.cart-subtotal').text('$' + subtotal.toFixed(2));

    // Update the full cart
    $('.full-cart').text('$' + subtotal.toFixed(2));
  }

  $(document).ready(function () {
    // Update cart count
    updateCartCount();
    // Call the updateCartTotals function when the page loads
    updateCartTotals();

    // Call the updateCartTotals function when a cart item is added or removed
    $(document).on('click', '.cart-remove', function () {
      updateCartCount();
      updateCartTotals();
    });

    $(document).on('change', '.cart-quantity input', function () {
      updateCartTotals();
    });

    $(document).on('change', '.csize option', function () {
      updateCartTotals();
    });
  });

  // Remove Cart Item
  function removeCartItem(event) {
    const buttonClicked = event.target;
    const tableRow = buttonClicked.closest('tr');
    const productName = tableRow.getElementsByClassName('cart-pro')[0].innerText;
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const productIndex = cart.findIndex(item => item.name === productName);
    if (productIndex > -1) {
      cart.splice(productIndex, 1)[0];
      localStorage.setItem('cart', JSON.stringify(cart));
      if (tableRow) {
        tableRow.remove();
      }
    }
  }

  // Quantity Changes
  function quantityChanged(event) {
    const input = event.target;
    if (isNaN(input.value) || input.value <= 0) {
      input.value = 1;
    }
  }

  // Register products from shop to sproduct
  const pro1 = document.querySelector('.pro1');
  if (pro1) {
    pro1.addEventListener('click', function () {
      const imgSrc = this.querySelector('.r-img').src;
      const category = this.querySelector('.Category').textContent;
      const productName = this.querySelector('.product').textContent;
      const price = this.querySelector('.shop-price').textContent;
      const description = this.querySelector('.main-desc').textContent;

      localStorage.setItem('imgSrc', imgSrc);
      localStorage.setItem('category', category);
      localStorage.setItem('productName', productName);
      localStorage.setItem('price', price);
      localStorage.setItem('description', description);

    });
  }

  // Populate product details in sproduct.html
  window.onload = function () {
    const productContainers = document.querySelectorAll('.pro');
    
    productContainers.forEach((container, index) => {
        container.addEventListener('click', function() {
            const mainImg = container.querySelector('img');
            const productName = container.querySelector('.product').textContent;
            const productPrice = container.querySelector('.shop-price').textContent;
            const category = container.querySelector('.Category').textContent;
            const description = container.querySelector('.main-desc').textContent;

            // Save data to local storage
            localStorage.setItem('imgSrc', mainImg.src);
            localStorage.setItem('productName', productName);
            localStorage.setItem('price', productPrice);
            localStorage.setItem('category', category);
            localStorage.setItem('description', description);
        });
    });

    // Populate product details in sproduct.html
    const mainImg = document.getElementById('MainImg');
    const productName = document.querySelector('.sprod-pro-name');
    const productPrice = document.querySelector('.sproduct-price');
    const category = document.querySelector('.sprod-category');
    const description = document.querySelector('.spro-main-desc');

    if (mainImg && productName && productPrice) {
        mainImg.src = localStorage.getItem('imgSrc');
        category.textContent = localStorage.getItem('category');
        productName.textContent = localStorage.getItem('productName');
        productPrice.textContent = localStorage.getItem('price');
        description.textContent = localStorage.getItem('description');
    }


    // Add product to cart in sproduct.html
    const addToCartButton = document.querySelector('#addCart');
    const selectedSize = document.querySelector('.s-size');
    const quantityInput = document.querySelector('.quantity');
    const errorPopup = document.getElementById('errorPopup');


    if (addToCartButton) {
      addToCartButton.addEventListener('click', function () {
        const productImage = mainImg.src;
        const name = productName.textContent.trim();
        let price = parseFloat(productPrice.textContent.slice(1));
        let pprice = parseFloat(productPrice.textContent.slice(1));
        const size = selectedSize.value;
        const quantity = parseInt(quantityInput.value);
        const isAlreadyInCart = cartData.some(item => item.name === name && item.size === size);
        
        if (!isAlreadyInCart) {
          // Increment cart count only if the product is not already in the cart
          cartCountElement.textContent = parseInt(cartCountElement.textContent) + 1;
        }

        if (isAlreadyInCart) {
          errorPopup.style.display = 'block';
          setTimeout(() => {
            errorPopup.style.display = 'none';
          }, 3000); // Hide error message after 3 seconds
          return; // Exit the function and don't proceed to add the item
        }

           // Increment cart count only if the product is not already in the cart
           cartCountElement.textContent = parseInt(cartCountElement.textContent) + 1;

        if (size === 'M') {
          pprice += 50;
        } else if (size === 'L') {
          pprice += 100;
        }

        const product = {
          image: productImage,
          name,
          price,
          pprice,
          size,
          quantity,
        };

        let existingCart = [];
        if (localStorage.getItem('cart')) {
          existingCart = JSON.parse(localStorage.getItem('cart'));
        }

        existingCart.push(product);

        localStorage.setItem('cart', JSON.stringify(existingCart));

        // Show success message
        document.getElementById('successPopup').style.display = 'block';
        setTimeout(() => {
          document.getElementById('successPopup').style.display = 'none';
        }, 3000); // Hide success message after 10 seconds
      });
    }
  };

  // Functionality for cart.html
  const cartData = JSON.parse(localStorage.getItem('cart')) || [];

  function generateCartItem(item) {
    const sizePrice = item.size === 'M' ? 50 : item.size === 'L' ? 100 : 0;
    return `
      <tr>
        <td><i class="bi bi-x-square-fill cart-remove"></i><a href="#"></a></td>
        <td><img src="${item.image}" alt="" class="cart-img"></td>
        <td class="cart-pro">${item.name}</td>
        <td class="cart-price">$${item.price}</td>
        <td class="cart-price1" style="display: none;">$${item.pprice}</td>
        <td class="cart-quantity"><input type="number" value="${item.quantity}" min="0"></td>
        <td class="cart-size">
          <select class="c-size">
            <option class="Small" ${item.size === 'S' ? 'selected' : ''}>S</option>
            <option class="Medium" ${item.size === 'M' ? 'selected' : ''}>M</option>
            <option class="Large" ${item.size === 'L' ? 'selected' : ''}>L</option>
          </select>
        </td>
        <td class="cart-total-price">$${((item.price + sizePrice) * item.quantity).toFixed(2)}</td>
      </tr>
    `;
  }

  const cartItemsHTML = cartData.map(generateCartItem).join('');

  if (document.querySelector('tbody')) {
    document.querySelector('tbody').innerHTML = cartItemsHTML;
  }

  const sizes = document.querySelectorAll('.c-size');
  const quantities = document.querySelectorAll('.cart-quantity input');
  const prices = document.querySelectorAll('.cart-price1');
  const totalPriceElements = document.querySelectorAll('.cart-total-price');

  sizes.forEach((size, index) => {
    let price = parseFloat(prices[index].innerText.replace('$', ''));
    const totalPriceElement = totalPriceElements[index];
    let lastSize = size.value;
    const quantity = quantities[index];
    let lastQuantity = parseInt(quantity.value);

    size.addEventListener('change', function () {
      const newSize = size.value;
      if ((lastSize === 'S' && newSize === 'M') || (lastSize === 'M' && newSize === 'L')) {
        price += 50;
      } else if (lastSize === 'S' && newSize === 'L') {
        price += 100;
      } else if ((lastSize === 'L' && newSize === 'M') || (lastSize === 'M' && newSize === 'S')) {
        price -= 50;
      } else if (lastSize === 'L' && newSize === 'S') {
        price -= 100;
      }
      lastSize = newSize;
      totalPriceElement.innerText = '$' + (price * quantity.value).toFixed(2);

      // Find the corresponding item in cartData and update its size and price
      const item = cartData[index];
      item.size = size.value;
      item.pprice = price;

      // Save the updated cartData to localStorage
      localStorage.setItem('cart', JSON.stringify(cartData));

      // Update the total price in the cart.html page
      let subtotal = 0;
      for (let i = 0; i < cartData.length; i++) {
        subtotal += cartData[i].pprice * cartData[i].quantity;
      }
      document.querySelector('.cart-subtotal').innerText = '$' + subtotal.toFixed(2);
      document.querySelector('.full-cart').innerText = '$' + subtotal.toFixed(2);
    });

    quantity.addEventListener('change', function () {
      const newQuantity = parseInt(quantity.value);
      if (newQuantity < lastQuantity) {
        totalPriceElement.innerText = '$' + (price * newQuantity).toFixed(2);
      } else {
        totalPriceElement.innerText = '$' + (price * newQuantity).toFixed(2);
      }
      lastQuantity = newQuantity;

      // Find the corresponding item in cartData and update its quantity
      const item = cartData[index];
      item.quantity = parseInt(quantity.value);

      // Save the updated cartData to localStorage
      localStorage.setItem('cart', JSON.stringify(cartData));
    });
  });
});
