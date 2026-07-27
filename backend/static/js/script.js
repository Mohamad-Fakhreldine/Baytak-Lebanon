const propertySelect = document.querySelector("#property-type");

new Choices(propertySelect, {
    searchEnabled: false,
    itemSelectText: "",
    shouldSort: false
});