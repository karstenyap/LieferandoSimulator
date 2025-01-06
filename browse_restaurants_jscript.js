$(document).ready(function() {
    // Trigger AJAX request when typing in the search input field
    $('#searchInput').on('input', function() {
        var searchQuery = $(this).val();  // Get the value of the search input
        
        // Send AJAX request to server with search query
        $.ajax({
            type: 'POST',
            url: '{{ url_for("browse_restaurants") }}',
            data: { search: searchQuery },
            success: function(response) {
                // Replace the restaurant list with the filtered result
                $('#restaurantList').html(response);
            }
        });
    });
});
