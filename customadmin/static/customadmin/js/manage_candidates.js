// Show confirmation message based on approval status
function confirmDelete(status) {
    if (status === true) {
        return confirm("This candidate is already APPROVED. Deleting will remove them from the voting dashboard. Are you sure?");
    } else if (status === false) {
        return confirm("This candidate is REJECTED. Are you sure you want to delete?");
    }
    return confirm("Are you sure you want to delete this pending candidate?");
}

// Handle theme preference
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('admin-theme');
    const checkbox = document.getElementById('themeToggle');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (checkbox) checkbox.checked = true;
    }
});
