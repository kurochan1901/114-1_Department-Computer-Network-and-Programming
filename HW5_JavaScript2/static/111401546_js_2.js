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

    //數量加減
    document.getElementById("cartTable").addEventListener("click", function(e) {
        const target = e.target;

        const row = target.closest("tr");
        if (!row) return;

        const quantitySpan = row.querySelector(".quantity span");
        const price = parseInt(row.querySelector(".price").textContent);
        const subtotal = row.querySelector(".subtotal");
        const stock = parseInt(row.querySelector(".stock").textContent);

        let quantity = parseInt(quantitySpan.textContent);

        if (target.classList.contains("plus")) {
            if (quantity < stock) {
                quantity++;
            }
        }
        if (target.classList.contains("minus")) {
            if (quantity > 0) {
                quantity--;
            }
        }
    
        quantitySpan.textContent = quantity;
        subtotal.textContent = price * quantity;

        updateTotal();    
    });
    
});
