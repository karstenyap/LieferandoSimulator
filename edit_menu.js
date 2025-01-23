// JavaScript to preview the image when selected
function previewImage(input, previewId) {
    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const preview = document.getElementById(previewId);
        preview.src = e.target.result;
    };

    if (file) {
        reader.readAsDataURL(file);
    }
}


// Function to handle menu item deletion
function deleteMenuItem(button) {
    const itemId = button.getAttribute('data-item-id');
    
    // Confirm deletion
    if (!confirm('Are you sure you want to delete this menu item?')) {
        return;
    }

    // Make the DELETE request
    fetch(`/delete_menu_item/${itemId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show notification
                const notification = document.getElementById('notification');
                notification.style.display = 'block';
                
                // Redirect to menu management after a delay
                setTimeout(() => {
                    window.location.href = '/menu_management';
                }, 3000); // 3 seconds delay
            } else {
                alert('Failed to delete the menu item. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
}

function showNotification() {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
}

function closeNotification() {
    const notification = document.getElementById('notification');
    notification.style.display = 'none';
}
