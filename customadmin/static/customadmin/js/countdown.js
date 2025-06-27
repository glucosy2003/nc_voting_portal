window.onload = function () {
  const toggle = document.getElementById('themeToggle');
  const theme = localStorage.getItem('darkMode');
  if (theme === 'true') {
    document.documentElement.setAttribute('data-theme', 'dark');
    toggle.checked = true;
  }

  toggle.addEventListener('change', function () {
    if (this.checked) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('darkMode', 'true');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('darkMode', 'false');
    }
  });
};
