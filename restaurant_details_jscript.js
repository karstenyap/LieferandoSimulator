// Fetch the current cart count and update the DOM
function updateCartCount() {
    $.ajax({
        url: "/cart_count", // Replace this with the Flask route that returns the cart count
        method: "GET",
        success: function (response) {
            $('#cart-count').text(response.cart_count || '0'); // Update cart count or default to 0
        },
        error: function (xhr) {
            console.error("Error fetching cart count:", xhr.responseText);
        }
    });
}

// Attach AJAX form submission for all add-to-cart forms
$(document).on("submit", ".add-to-cart-form", function (event) {
    event.preventDefault(); // Prevent default form submission

    const form = $(this);
    const url = form.attr("action");

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // Serialize form data
        success: function (response) {
            updateCartCount(); // Update the cart count dynamically
        },
        error: function (xhr) {
            console.error("Error adding item to cart:", xhr.responseText);
        }
    });
});

// On page load, fetch the initial cart count
window.addEventListener('load', () => {
    updateCartCount(); // Update the cart count on page load
});
