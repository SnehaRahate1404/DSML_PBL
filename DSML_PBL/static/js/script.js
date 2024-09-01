const wish = document.querySelector(".wishes");
// const clock = document.querySelector(".clock");
const time = document.querySelector(".time");

function updateGreeting() {
    let date = new Date();
    let hours = date.getHours();
    let greeting;

    if (hours >= 5 && hours < 12) {
        greeting = "Good Morning";
    } else if (hours >= 12 && hours < 17) {
        greeting = "Good Afternoon";
    } else if (hours >= 17 && hours < 21) {
        greeting = "Good Evening";
    } else {
        greeting = "Good Night";
    }

    time.innerHTML = greeting;
}

// function updateClock() {
//     let date = new Date();
//     clock.innerHTML = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
// }

setInterval(function() {
    // updateClock();
    updateGreeting();
}, 1000);

// Initial call to set greeting on page load
updateGreeting();

document.addEventListener('DOMContentLoaded', () => {
    const micImg = document.querySelector('.mic-button');
    const circles = document.querySelector('.circles');
    const timerDisplay = document.querySelector('.timer');
    
    let timer;
    let seconds = 0;

    micImg.addEventListener('click', () => {
        circles.style.display = 'block';
        seconds = 0;
        timerDisplay.textContent = formatTime(seconds);
        
        clearInterval(timer); // Clear any existing timer
        
        timer = setInterval(() => {
            seconds++;
            timerDisplay.textContent = formatTime(seconds);
        }, 1000);
    });

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
});
