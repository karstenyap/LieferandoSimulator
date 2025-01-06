// Submit remarks dynamically
$(document).on("submit", "#remark-form", function (event) {
    event.preventDefault();
    const form = $(this);

    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        success: function () {
            alert("Remark saved successfully!");
        },
        error: function (xhr) {
            console.error("Error saving remark:", xhr.responseText);
        }
    });
});
