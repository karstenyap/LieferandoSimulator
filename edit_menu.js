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
