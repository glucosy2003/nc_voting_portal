// Placeholder for dashboard-specific JS
// All global functions like toggleTheme and dark mode handling are now in global.js
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('hamburger-toggle');
    const sidebar = document.getElementById('admin-sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    const closeBtn = document.getElementById('close-sidebar');

    function openSidebar() {
        sidebar.classList.add('active');
        backdrop.classList.add('active');
    }

    function closeSidebar() {
        sidebar.classList.remove('active');
        backdrop.classList.remove('active');
    }

    toggleBtn.addEventListener('click', openSidebar);
    closeBtn.addEventListener('click', closeSidebar);
    backdrop.addEventListener('click', closeSidebar);
});
