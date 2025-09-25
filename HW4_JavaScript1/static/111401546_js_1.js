let answer = Math.floor(Math.random() * 101);
let count = 0;
console.log(answer);

function guessNumber() {
    const guessInput = parseInt(document.getElementById("guessInput").value);
    count++;

    if (isNaN(guessInput)) {
        alert("請輸入一個有效的數字！");
        return;
    };

};