console.log("Pomodoro Connected!");

// ===========================
// DOM ELEMENTS
// ===========================

const timer = document.getElementById("timer");
const startBtn = document.getElementById("startBtn");
const pauseBtn = document.getElementById("pauseBtn");
const resetBtn = document.getElementById("resetBtn");

const focusInput = document.querySelectorAll(".time-input")[0];
const breakInput = document.querySelectorAll(".time-input")[1];

const progressBar = document.querySelector(".progress-bar");
const sessionText = document.querySelector(".session-type");

// ===========================
// PROGRESS RING
// ===========================

const radius = 145;
const circumference = 2 * Math.PI * radius;

progressBar.style.strokeDasharray = circumference;
progressBar.style.strokeDashoffset = 0;

// ===========================
// TIMER VARIABLES
// ===========================

let interval = null;

let isBreak = false;

let totalTime = Number(focusInput.value) * 60;

let timeLeft = totalTime;

// ===========================
// UPDATE TIMER
// ===========================

function updateTimer(){

    let minutes = Math.floor(timeLeft / 60);

    let seconds = timeLeft % 60;

    if(seconds < 10){

        seconds = "0" + seconds;

    }

    timer.textContent = `${minutes}:${seconds}`;

    updateProgressRing();

}

// ===========================
// UPDATE PROGRESS RING
// ===========================

function updateProgressRing(){

    const progress = timeLeft / totalTime;

    progressBar.style.strokeDashoffset =
        circumference * (1 - progress);

}

// ===========================
// START TIMER
// ===========================

function startTimer(){

    if(interval !== null) return;

    interval = setInterval(function(){

        if(timeLeft > 0){

            timeLeft--;

            updateTimer();

        }
        else{

            clearInterval(interval);

            interval = null;

            changeSession();

        }

    },1000);

}

// ===========================
// PAUSE TIMER
// ===========================

function pauseTimer(){

    clearInterval(interval);

    interval = null;

}

// ===========================
// RESET TIMER
// ===========================

function resetTimer(){

    pauseTimer();

    if(isBreak){

        totalTime = Number(breakInput.value) * 60;

    }
    else{

        totalTime = Number(focusInput.value) * 60;

    }

    timeLeft = totalTime;

    updateTimer();

}
// ===========================
// CHANGE SESSION
// ===========================

function changeSession(){

    if(!isBreak){

        isBreak = true;

        totalTime = Number(breakInput.value) * 60;
        timeLeft = totalTime;

        sessionText.textContent = "☕ Break Time";

        updateTimer();

        // Automatically start break
        startTimer();

    }
    else{

        isBreak = false;

        totalTime = Number(focusInput.value) * 60;
        timeLeft = totalTime;

        sessionText.textContent = "🍅 Focus Session";

        updateTimer();

        fetch("/save-focus", {

          method: "POST",

          headers: {
          "Content-Type": "application/json"
          },

          body: JSON.stringify({
          minutes: Number(focusInput.value)
          })

        });

        alert("🎉 One Pomodoro Cycle Completed!");

    }

}

// ===========================
// BUTTON EVENTS
// ===========================

startBtn.addEventListener("click", function(){

    startTimer();

});

pauseBtn.addEventListener("click", function(){

    pauseTimer();

});

resetBtn.addEventListener("click", function(){

    isBreak = false;

    sessionText.textContent = "🍅 Focus Session";

    resetTimer();

});

// ===========================
// INPUT EVENTS
// ===========================

focusInput.addEventListener("change", function(){

    if(interval !== null) return;

    if(!isBreak){

        totalTime = Number(focusInput.value) * 60;
        timeLeft = totalTime;

        updateTimer();

    }

});

breakInput.addEventListener("change", function(){

    if(interval !== null) return;

    if(isBreak){

        totalTime = Number(breakInput.value) * 60;
        timeLeft = totalTime;

        updateTimer();

    }

});

// ===========================
// INITIALIZE
// ===========================

updateTimer();