document.addEventListener('DOMContentLoaded', function () {
    // Function to validate if the restaurant is open for at least 3 hours
    function isValidTimeRange(openTime, closeTime) {
        const [openHours, openMinutes] = openTime.split(':').map(Number);
        const [closeHours, closeMinutes] = closeTime.split(':').map(Number);

        // Convert times to minutes for easy comparison
        const openTotalMinutes = openHours * 60 + openMinutes;
        const closeTotalMinutes = closeHours * 60 + closeMinutes;

        // Check if the time difference is at least 180 minutes (3 hours)
        return closeTotalMinutes - openTotalMinutes >= 180;
    }

    // Function to validate the form before submission
    function validateForm(event) {
        let atLeastOneOpen = false;
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

        for (const day of days) {
            const openTime = document.getElementById(`${day}_open`).value;
            const closeTime = document.getElementById(`${day}_close`).value;
            const isClosed = document.getElementById(`${day}_closed`).checked;

            if (isClosed) {
                continue; // Skip validation for closed days
            }

            // Check if both times are entered
            if (!openTime || !closeTime) {
                alert(`Please enter both opening and closing times for ${day}.`);
                return false;
            }

            // Check if open duration is at least 3 hours
            if (!isValidTimeRange(openTime, closeTime)) {
                alert(`The restaurant must be open for at least 3 hours on ${day}.`);
                return false;
            }

            atLeastOneOpen = true;
        }

        if (!atLeastOneOpen) {
            alert("Your restaurant must be open for at least one day.");
            return false;
        }

        return true;
    }

    // Attach the validateForm function to the form's submit event
    document.getElementById('openingHoursForm').addEventListener('submit', function (event) {
        if (!validateForm(event)) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });

    // Function to toggle the "Closed" checkbox state and duck animation
    function toggleDuck(day) {
        const isClosed = document.getElementById(`${day}_closed`).checked;
        const openInput = document.getElementById(`${day}_open`);
        const closeInput = document.getElementById(`${day}_close`);
        const duckContainer = document.getElementById(`${day}_duck`);

        openInput.disabled = isClosed;
        closeInput.disabled = isClosed;

        // Show/hide the "sleeping duck" based on closed state
        if (isClosed) {
            duckContainer.querySelector('.sleeping-duck').classList.add('visible');
        } else {
            duckContainer.querySelector('.sleeping-duck').classList.remove('visible');
        }
    }

    // Attach toggleDuck to each day's "Closed" checkbox
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    for (const day of days) {
        document.getElementById(`${day}_closed`).addEventListener('change', () => toggleDuck(day));
    }
});
