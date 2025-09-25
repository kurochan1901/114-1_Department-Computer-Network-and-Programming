let answer = Math.floor(Math.random() * 101);
let min = 0;
let max = 100;
let count = 0;
console.log(answer);

function guessNumber() {
    const guessInput = parseInt(document.getElementById("guessInput").value);
    count++;

    if (isNaN(guessInput)){
        alert("請輸入一個有效的數字！");
        return;
    };

    if (guessInput < 0 || guessInput > 100) {
        alert("請輸入0到100之間的數字！");
        return;
    };
    if (guessInput > answer) {
        max = guessInput;
        alert(`太大了，介於${min} ~ ${max}之間`);
    }else if (guessInput < answer) {
        min = guessInput;
        alert(`太小了，介於${min} ~ ${max}之間`);
    }else {
        alert(`恭喜你答對了！答案是${answer}。你總共猜了${count}次。`);
        answer = Math.floor(Math.random() * 101);
        min = 0;
        max = 100;
        count = 0;
    };

};