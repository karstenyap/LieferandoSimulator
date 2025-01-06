// Function to preview the image before upload
function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            preview.src = reader.result;
            preview.classList.add('visible'); // Add 'visible' class to show the preview
        };
        reader.readAsDataURL(file);
    }
}

// Update word count for description input
function updateWordCount() {
    const descriptionField = document.getElementById('description');
    const wordCount = descriptionField.value.trim().split(/\s+/).filter(function(word) {
        return word.length > 0;
    }).length;

    // Update the word count display
    document.getElementById('description-word-count').textContent = wordCount + '/100 words';

    // Optionally, change text color if the word count is close to the limit
    if (wordCount > 100) {
        document.getElementById('description-word-count').style.color = 'red';
    } else {
        document.getElementById('description-word-count').style.color = 'black';
    }
}

// Form validation before submission
function validateForm() {
    const restaurantName = document.getElementById('restaurant-name').value.trim();
    const password = document.getElementById('password').value.trim();
    const description = document.getElementById('description').value.trim();

    // Validate restaurant name (Max 10 words)
    const nameWords = restaurantName.split(/\s+/).filter(word => word.length > 0).length;
    if (nameWords > 30) {
        alert('Restaurant name cannot exceed 30 words');
        return false; // Prevent form submission
    }

    // Validate password (At least 8 characters)
    if (password.length < 8) {
        alert('Password must be at least 8 characters long');
        return false; // Prevent form submission
    }

    // Validate description (Should not exceed 100 words)
    const descriptionWords = description.split(/\s+/).filter(word => word.length > 0).length;
    if (descriptionWords > 100) {
        alert('Description cannot exceed 100 words');
        return false; // Prevent form submission
    }

    // No errors, allow form submission
    return true;
}



// Handle form submission
document.getElementById('restaurant-register-form').addEventListener('submit', function (e) {
    // Prevent form from being submitted if validation fails
    if (!validateForm()) {
        e.preventDefault(); // Prevent default form submission
        return false;
    }

    // If validation is successful, alert user and proceed
    alert('Form submitted successfully! Proceeding to the next step.');
    // You can add further logic here to handle actual form submission, e.g., AJAX request.
});
