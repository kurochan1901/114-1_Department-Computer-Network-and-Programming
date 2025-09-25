document.write(`
    <style>
        input {
            width: 200px;
            height: 40px;
            font-size: 24px;
            text-align: right;
        }
        button {
            width: 50px;
            height: 60px;
            font-size: 24px;
            margin: 3px;
        }
    </style>
    `);

document.write('<input type="text" id="display" readonly><br><br>'); // 顯示輸入和結果的欄位
for (let i=9; i>=0; i--) {
    document.write(`<button onclick="appendNumber('${i}')">${i}</button>`); // 數字按鈕
    if (i===7||i===4||i===1) document.write('<br>');
}
document.write('<button onclick="clearDisplay()" style="width:106px">Clear</button>');
document.write('<br><br>');

const operators = ['+', '-', '*', '/', '(', ')'];
for (let op of operators) {
  document.write(`<button onclick="append('${op}')">${op}</button>`);
};

document.write('<br><button onclick="calculate()" style="width:106px">Enter</button>');
