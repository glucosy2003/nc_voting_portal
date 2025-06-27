document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.documentElement.dataset.theme = currentTheme;
    }

    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.checked = currentTheme === 'dark';
    }
});
