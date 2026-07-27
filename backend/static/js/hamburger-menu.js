const menuToggle = document.querySelector(".menu-toggle");
const menuPopup = document.querySelector(".menu-popup");

menuToggle.addEventListener("click", (event) => {
    event.stopPropagation();
    menuPopup.classList.toggle("active");
});

document.addEventListener("click", () => {
    menuPopup.classList.remove("active");
});

menuPopup.addEventListener("click", (event) => {
    event.stopPropagation();
});