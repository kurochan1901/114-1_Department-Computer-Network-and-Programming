let answer = Math.floor(Math.random() * 101);
let min = 0;
let max = 100;
let count = 0;
let startTime = null;
let timerInterval = null;
console.log(answer);

function guessNumber() {
    const guessInput = parseInt(document.getElementById("guessInput").value);
    const hint = document.getElementById("hint");
    const timerDisplay = document.getElementById("timer");
    count++;

    //計時開始
    if (!startTime){
        startTime = new Date();
        timerInterval = setInterval( () => {
            const now = new Date();
            const timePassed = Math.floor((now - startTime) / 1000);
            timerDisplay.textContent = `已經過：${timePassed}秒`;
        } )
    }

    // 判斷數字大小
    if (isNaN(guessInput)){
        hint.textContent = "請輸入一個有效的數字！";
        return;
    };

    if (guessInput < 0 || guessInput > 100) {
        hint.textContent = "請輸入0到100之間的數字！";
        return;
    };
    if (guessInput > answer) {
        max = guessInput;
        hint.textContent = `太大了，介於${min} ~ ${max}之間`;
    }else if (guessInput < answer) {
        min = guessInput;
        hint.textContent = `太小了，介於${min} ~ ${max}之間`;
    }else {
        alert(`恭喜你答對了！答案是${answer}。\n你總共猜了${count}次。`);
        answer = Math.floor(Math.random() * 101);
        min = 0;
        max = 100;
        count = 0;
    };

};