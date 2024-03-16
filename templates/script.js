document.addEventListener("DOMContentLoaded", function () {
    // Hide loader overlay and show content when the page has fully loaded
    window.addEventListener('load', function () {
        var loaderOverlay = document.querySelector('.loader-overlay');
        var content = document.querySelector('.content');
        loaderOverlay.style.display = 'none';
        content.style.display = 'block';
    });
});
