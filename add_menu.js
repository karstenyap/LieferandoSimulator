let itemCount = 1;

// Add Menu Item Button Event
document.getElementById('add-menu-item-btn').addEventListener('click', () => {
    const container = document.getElementById('menu-items-container');
    const newItem = document.getElementById('menu-item-0').cloneNode(true);

    updateMenuItemFields(newItem, itemCount);
    container.appendChild(newItem);
    itemCount++;
});

function deleteLastMenuItem() {
    const items = document.querySelectorAll('.menu-item');
    if (items.length > 1) { // Prevent deleting the last item
        items[items.length - 1].remove();
        itemCount--;
    }
}

function updateMenuItemFields(item, index) {
    item.id = `menu-item-${index}`;
    const fields = ['item_name', 'price', 'description', 'image'];

    fields.forEach(field => {
        const input = item.querySelector(`#${field}_0`);
        input.id = `${field}_${index}`;
        input.name = `${field}[]`;
        input.value = ''; // Clear cloned values
        if (field === 'image') {
            const preview = item.querySelector(`#image-preview-0`);
            const uploadText = item.querySelector(`#upload-text-0`);
            preview.id = `image-preview-${index}`;
            uploadText.id = `upload-text-${index}`;
            input.setAttribute('onchange', `previewImage(this, 'image-preview-${index}', 'upload-text-${index}')`);
        }
    });
}

function previewImage(input, previewId, uploadTextId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    const uploadText = document.getElementById(uploadTextId);

    if (file) {
        const reader = new FileReader();
        reader.onload = e => {
            preview.src = e.target.result;
            preview.style.display = 'block';
            uploadText.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
}
