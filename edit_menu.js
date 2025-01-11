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

function deleteMenuItem(button) {
    var itemId = button.getAttribute('data-item-id');

    fetch('/delete_menu_item/' + itemId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const notification = document.getElementById('notification');
            notification.style.display = 'block';
            notification.innerHTML = `<p>${data.message} Please return to the <a href="/menu_management">menu management</a> page.</p>`;
        } else {
            alert('Failed to delete menu item.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the menu item.');
    });
}
