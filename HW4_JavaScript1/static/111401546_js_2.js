document.write('<input type="text" id="display" readonly><br><br>'); // 顯示輸入和結果的欄位
for (let i=9; i>=0; i--) {
    document.write(`<button onclick="appendNumber('${i}')">${i}</button>`); // 數字按鈕
    if (i===7||i===4||i===1) document.write('<br>');
}