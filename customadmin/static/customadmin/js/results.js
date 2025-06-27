// Auto-refresh the page every 15 seconds
setTimeout(() => {
  location.reload();
}, 15000);

// Toggle light/dark theme
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  localStorage.setItem("adminTheme", next);
}

// Restore theme on load
window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("adminTheme");
  if (saved) {
    document.documentElement.setAttribute("data-theme", saved);
    const toggle = document.getElementById("themeToggle");
    if (toggle) toggle.checked = saved === "dark";
  }
});
