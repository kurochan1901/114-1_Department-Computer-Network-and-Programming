document.addEventListener("DOMContentLoaded", () => {
    const selectAll = document.getElementById("selectAll");
    const itemCheckboxes = document.querySelectorAll(".itemCheckbox");


    //全選
    selectAll.addEventListener("change", () => {
        itemCheckboxes.forEach(cb => cb.checked = selectAll.checked);
        updateTotal();
    });
    //全選單選連動
    itemCheckboxes.forEach(cb => {
        cb.addEventListener("change", () => {
        const allChecked = [...itemCheckboxes].every(cb => cb.checked);
        selectAll.checked = allChecked;
        updateTotal();
        });
    });
});

//數量加減
document.querySelectorAll("tr").forEach(row => {
    const minusBtn = row.querySelector(".minus");
    const plusBtn = row.querySelector(".plus");
    const quantityInput = row.querySelector(".quantity");

    minusBtn.addEventListener("click", () => {
        let quantity = parseInt(quantityInput.textContent);
        if (quantity > 1) quantity--;
        quantityInput.textContent = quantity;
        updateTotal();
    });

    plusBtn.addEventListener("click", () => {
        let quantity = parseInt(quantityInput.textContent);
        quantity++;
        quantityInput.textContent = quantity;
        updateTotal();
    });

});