let remaining = Number(window.SESSION_TIME || 0);
const timerEl = document.getElementById("timer");

if (timerEl && remaining > 0) {

    function updateTimer() {
        const min = Math.floor(remaining / 60);
        const sec = remaining % 60;

        timerEl.textContent = `${min}m ${sec}s`;

        if (remaining <= 0) {
            window.location.href = "/logout";
        } else {
            remaining--;
        }
    }

    updateTimer();
    setInterval(updateTimer, 1000);
}



