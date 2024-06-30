document.addEventListener('DOMContentLoaded', function () {
    const loregBox = document.querySelector('.logreg-box');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const successPopup = document.querySelector('.success-popup');
    const errorPopupForm = document.getElementById('errorPopupForm'); // Assuming ID for signup form errors
  
    if (loregBox && loginLink && registerLink) {
      registerLink.addEventListener('click', function () {
        loregBox.classList.add('active');
      });
  
      loginLink.addEventListener('click', function () {
        loregBox.classList.remove('active');
      });
    }
  });
  