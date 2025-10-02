//選取方塊
const selectAll = document.getElementById("selectAll");
const itemCheckboxes = document.querySelectorAll(".itemCheckbox");

selectAll.addEventListener("change", () => {
    itemCheckboxes.forEach(cb => cb.checked = selectAll.checked);
    updateTotal();
});

itemCheckboxes.forEach(cb => {
    cb.addEventListener("change", () => {
    const allChecked = [...itemCheckboxes].every(cb => cb.checked);
    selectAll.checked = allChecked;
    updateTotal();
    });
});