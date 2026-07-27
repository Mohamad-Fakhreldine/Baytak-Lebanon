const filterButton = document.getElementById("open-filters");
const filterOverlay = document.getElementById("filter-overlay");
const cancelButton = document.getElementById("cancel-filters");
const applyButton = document.getElementById("apply-filters");

function openFilterPopup() {
    filterOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeFilterPopup() {
    filterOverlay.classList.remove("active");
    document.body.style.overflow = "";
}

filterButton.addEventListener("click", () => {
    openFilterPopup();
});

cancelButton.addEventListener("click", () => {
    closeFilterPopup();
});

applyButton.addEventListener("click", () => {
    closeFilterPopup();
});