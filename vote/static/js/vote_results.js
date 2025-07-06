function scrollLeft(btn) {
  const container = btn.nextElementSibling;
  container.scrollBy({ left: -300, behavior: "smooth" });
}
function scrollRight(btn) {
  const container = btn.previousElementSibling;
  container.scrollBy({ left: 300, behavior: "smooth" });
}
