document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    const newPass = form.new_password1.value;
    const confirmPass = form.new_password2.value;
    if (newPass !== confirmPass) {
      alert("New passwords do not match.");
      e.preventDefault();
    }
  });
});
