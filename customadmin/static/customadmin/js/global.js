function toggleTheme() {
  const darkMode = localStorage.getItem("darkMode") === "true";
  if (darkMode) {
    document.documentElement.setAttribute("data-theme", "light");
    localStorage.setItem("darkMode", "false");
  } else {
    document.documentElement.setAttribute("data-theme", "dark");
    localStorage.setItem("darkMode", "true");
  }
}

window.onload = function () {
  const toggle = document.getElementById("themeToggle");
  const isDark = localStorage.getItem("darkMode") === "true";
  if (isDark) {
    document.documentElement.setAttribute("data-theme", "dark");
    if (toggle) toggle.checked = true;
  }
};


document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".edit-student-form");
    form.addEventListener("submit", () => {
        console.log("Submitting updated student data...");
    });
});

