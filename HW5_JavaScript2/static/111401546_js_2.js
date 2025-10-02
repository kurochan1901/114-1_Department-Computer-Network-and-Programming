//全域監聽click
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

        const quantityInput = row.querySelector(".quantityInput");
        const price = parseInt(row.querySelector(".price").textContent);
        const subtotal = row.querySelector(".subtotal");
        const stock = parseInt(row.querySelector(".stock").textContent);

        let quantity = parseInt(quantityInput.value);

        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
        }
        if (quantity > stock) {
            quantity = stock;
        }

        if (target.classList.contains("plus")) {
            if (quantity < stock) {
                quantity++;
            }
        }
        if (target.classList.contains("minus")) {
            if (quantity > 1) {
                quantity--;
            }
        }

        quantityInput.value = quantity;
        subtotal.textContent = price * quantity;

        updateTotal();    
    });

    function updateTotal() {
        let total = 0;
        document.querySelectorAll("#cartTable tbody tr").forEach(row => {
            const checkboxSlct = row.querySelector(".itemCheckbox");
            const subtotalSlct = row.querySelector(".subtotal");
            if (!checkboxSlct || !subtotalSlct) return;

            const subtotal = parseInt(subtotalSlct.textContent);
            if (checkboxSlct.checked && !isNaN(subtotal)) {
                total += subtotal;
            }
        });
        document.getElementById("total").textContent = total;
    }

    //結帳
    document.getElementById("checkoutBtn").addEventListener("click", () => {
        const totalnum = parseInt(document.getElementById("total").textContent);
        if (totalnum <= 0) return;

        let summary = `購買明細：\n`;
        document.querySelectorAll("#cartTable tbody tr").forEach(row => {
            const checkbox = row.querySelector(".itemCheckbox");
            if (!checkbox || !checkbox.checked) return;
        
            const name = row.querySelector(".productName").textContent.trim();
            const quantityInput = row.querySelector(".quantityInput");
            const quantity = parseInt(quantityInput.value);
            const stockCell = row.querySelector(".stock");
            let stock = parseInt(stockCell.textContent);

            summary += `商品：${name}，數量：${quantity}\n`;

            stock -= quantity;
            if (stock < 0) stock = 0;
            stockCell.textContent = stock;
            
            if (stock > 0) {
                quantityInput.value = 1;
            } else {
                quantityInput.value = 0;
            }
            checkbox.checked = false;
            const price = parseInt(row.querySelector(".price").textContent);
            row.querySelector(".subtotal").textContent = price * parseInt(quantityInput.value);
        });

        alert(summary + `總金額：${totalnum} 元`);
        document.getElementById("selectAll").checked = false;
        updateTotal();
    });

});
