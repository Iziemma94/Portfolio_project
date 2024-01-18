// scripts.js

// Function to handle a specific action
function handleButtonClick() {
    alert('Button clicked!');
    // Add more code here for additional actions
}

// Smooth scrolling to anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Toggle mobile navigation menu
var mobileMenuButton = document.getElementById('mobileMenuButton');
var mobileMenu = document.getElementById('mobileMenu');

if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function () {
        mobileMenu.classList.toggle('show');
    });
}

// Show and hide modal windows
var modalButton = document.getElementById('modalButton');
var modal = document.getElementById('modal');

if (modalButton && modal) {
    modalButton.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Find the button element by its ID
    var myButton = document.getElementById('myButton');

    // Check if the button element is found
    if (myButton) {
        // Add a click event listener to the button
        myButton.addEventListener('click', handleButtonClick);
    }

    // You can add more code here for other interactions or functionalities
});
