// main.js - General UI logic

document.addEventListener('DOMContentLoaded', function() {
    // Highlight active sidebar link
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        if (window.location.pathname === link.getAttribute('href')) {
            link.classList.add('active');
        }
    });
});
