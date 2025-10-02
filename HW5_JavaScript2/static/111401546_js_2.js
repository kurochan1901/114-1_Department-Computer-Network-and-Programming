document.addEventListener("DOMContentLoaded", () => {
    const selectAll = document.getElementById("selectAll");
    const itemCheckboxes = document.querySelectorAll(".itemCheckbox");


    //全選
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
});