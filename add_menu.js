// Initialize Item Count
let itemCount = 1;

// Add Menu Item Button Event
document.getElementById('add-menu-item-btn').addEventListener('click', () => {
    const container = document.getElementById('menu-items-container');
    const newItem = document.getElementById('menu-item-0').cloneNode(true);

    updateMenuItemFields(newItem, itemCount);
    container.appendChild(newItem);
    itemCount++;
});

// Delete Last Menu Item Button
function deleteLastMenuItem() {
    const items = document.querySelectorAll('.menu-item');
    if (items.length > 0) { // Allow deleting all items
        items[items.length - 1].remove();
        itemCount--;
    }
}

function updateMenuItemFields(item, index) {
    const fields = ['item_name', 'price', 'description', 'image'];

    fields.forEach(field => {
        const input = item.querySelector(`#${field}_0`);
        input.id = `${field}_${index}`;  // Unique ID for each input
        input.name = `${field}[]`;        // Ensure the name stays as an array
        input.value = '';                 // Clear the value in cloned fields

        if (field === 'description') {
            input.nextElementSibling.id = `description-word-count-${index}`;
            input.nextElementSibling.textContent = '0/100 words';
        } else if (field === 'image') {
            const preview = item.querySelector(`#image-preview-0`);
            preview.id = `image-preview-${index}`;
            input.setAttribute('onchange', `previewImage(this, 'image-preview-${index}')`);
        }
    });
}


// Image Preview Functionality
function previewImage(input, previewId, uploadTextId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    const uploadText = document.getElementById(uploadTextId);

    if (file) {
        const reader = new FileReader();

        reader.onload = e => {
            preview.src = e.target.result;
            preview.style.display = 'block'; // Show the image preview
            uploadText.style.display = 'none'; // Hide the "Click to Upload" text
        };

        reader.readAsDataURL(file);
    } else {
        // If no file is selected, reset to default
        preview.src = '';
        preview.style.display = 'none';
        uploadText.style.display = 'block';
    }
}
