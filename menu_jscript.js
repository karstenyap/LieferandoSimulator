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
    if (items.length > 1) {
        items[items.length - 1].remove();
    } else {
        alert('At least one menu item is required.');
    }
}

// Function to Update Cloned Menu Item
function updateMenuItemFields(item, index) {
    const fields = ['item_name', 'price', 'description', 'image'];

    fields.forEach(field => {
        const input = item.querySelector(`#${field}_0`);
        input.id = `${field}_${index}`;
        input.name = `${field}[]`;
        input.value = '';

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
function previewImage(input, previewId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    const reader = new FileReader();

    reader.onload = e => preview.src = e.target.result;
    if (file) reader.readAsDataURL(file);
}

// Form Validation
function validateForm() {
    const menuItems = document.querySelectorAll('.menu-item');
    if (menuItems.length === 0) {
        alert('You must add at least one menu item.');
        return false;
    }
    return true;
}
