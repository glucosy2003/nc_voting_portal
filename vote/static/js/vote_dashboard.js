// ===============================
// Card Flip Logic
// ===============================
function flipCard(card) {
    card.classList.toggle('flipped');
}

// ===============================
// Voting Confirmation Prompt
// ===============================
function confirmVote(event) {
    event.preventDefault();
    const form = event.target.closest('form');

    Swal.fire({
        title: 'Confirm Your Vote',
        text: 'Are you sure you want to vote for this candidate?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, Vote',
        cancelButtonText: 'Cancel',
        reverseButtons: true,
        background: document.documentElement.dataset.theme === 'dark' ? '#1f1f1f' : '#fff',
        color: document.documentElement.dataset.theme === 'dark' ? '#fff' : '#333',
        confirmButtonColor: '#d97706',
        cancelButtonColor: '#6b7280',
    }).then((result) => {
        if (result.isConfirmed) form.submit();
    });
}

// ===============================
// Audio Control
// ===============================
function toggleAudio() {
    const audio = document.getElementById("votingSong");
    const isPlaying = localStorage.getItem("votingSongPlaying") === "true";
    isPlaying ? audio.pause() : audio.play();
    localStorage.setItem("votingSongPlaying", !isPlaying);
    updateAudioButton();
}

function updateAudioButton() {
    const btn = document.getElementById("audioToggle");
    const isPlaying = localStorage.getItem("votingSongPlaying") === "true";
    if (btn) btn.textContent = isPlaying ? "⏸️ Pause Voting Song" : "▶️ Play Voting Song";
}

document.addEventListener("DOMContentLoaded", () => {
    const audio = document.getElementById("votingSong");
    if (localStorage.getItem("votingSongPlaying") === "true") {
        audio.play().catch(() => {});
    }
    updateAudioButton();

    // Set theme toggle
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.dataset.theme = savedTheme;
        const toggle = document.getElementById("themeToggle");
        if (toggle) toggle.checked = savedTheme === 'dark';
    }
});

// ===============================
// Countdown Timers
// ===============================
if (typeof votingStatus !== 'undefined' && votingStatus === 'open') {
    let timeLeft = parseInt(votingTimeRemaining) || 0;
    const timerEl = document.getElementById('countdown');
    let votingExpiredShown = false;

    function updateCountdown() {
        if (!timerEl) return;

        if (timeLeft <= 0 && !votingExpiredShown) {
            votingExpiredShown = true;
            timerEl.textContent = '00:00:00';
            Swal.fire({
                icon: 'info',
                title: 'Voting Ended',
                text: 'Voting has ended. Reloading...',
                timer: 4000,
                showConfirmButton: false
            }).then(() => {
                const resultsUrl = document.getElementById("resultsUrl")?.dataset.url;
                if (resultsUrl) window.location.href = resultsUrl;
            });
            return;
        }

        const hrs = Math.floor(timeLeft / 3600);
        const mins = Math.floor((timeLeft % 3600) / 60);
        const secs = timeLeft % 60;
        timerEl.textContent = `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        timeLeft--;
        setTimeout(updateCountdown, 1000);
    }

    updateCountdown();
}

if (typeof applicationStatus !== 'undefined' && applicationStatus === 'open') {
    let appTimeLeft = parseInt(applicationTimeRemaining) || 0;
    const appTimer = document.getElementById('applicationCountdown');

    function updateAppCountdown() {
        if (!appTimer) return;

        if (appTimeLeft <= 0) {
            appTimer.textContent = '00:00:00';
            return;
        }

        const h = Math.floor(appTimeLeft / 3600);
        const m = Math.floor((appTimeLeft % 3600) / 60);
        const s = appTimeLeft % 60;
        appTimer.textContent = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        appTimeLeft--;
        setTimeout(updateAppCountdown, 1000);
    }

    updateAppCountdown();
}

// ===============================
// Manifesto Toggle
// ===============================
function toggleManifesto(button) {
    const container = button.closest('.candidate-card').querySelector('.manifesto-container');
    container.classList.toggle('expanded');
    button.textContent = container.classList.contains('expanded') ? 'See less' : 'See more';
}

// ===============================
// Horizontal Scrollable Cards
// ===============================
function scrollLeft(btn) {
    const container = btn.parentElement.querySelector('.scrollable-cards');
    container.scrollBy({ left: -300, behavior: 'smooth' });
    setTimeout(() => updateScrollArrows(container), 400);
}

function scrollRight(btn) {
    const container = btn.parentElement.querySelector('.scrollable-cards');
    container.scrollBy({ left: 300, behavior: 'smooth' });
    setTimeout(() => updateScrollArrows(container), 400);
}

function updateScrollArrows(container) {
    const leftBtn = container.parentElement.querySelector('.scroll-btn.left');
    const rightBtn = container.parentElement.querySelector('.scroll-btn.right');
    const scrollLeft = container.scrollLeft;
    const scrollWidth = container.scrollWidth;
    const clientWidth = container.clientWidth;
    const atStart = scrollLeft <= 5;
    const atEnd = scrollLeft + clientWidth >= scrollWidth - 5;

    if (leftBtn) leftBtn.classList.toggle('visible', !atStart);
    if (rightBtn) rightBtn.classList.toggle('visible', !atEnd);
}

// ===============================
// Center Cards If Not Scrollable
// ===============================
function updateCardCentering(container) {
    const cards = container.querySelectorAll('.candidate-card');
    let totalWidth = 0;
    cards.forEach(card => totalWidth += card.offsetWidth + 16);
    container.style.setProperty('--cards-width', totalWidth + 'px');
    if (totalWidth < container.clientWidth) {
        container.classList.add('centered');
    } else {
        container.classList.remove('centered');
    }
}

// Init all scroll areas
document.addEventListener('DOMContentLoaded', () => {
    const scrollableAreas = document.querySelectorAll('.scrollable-cards');
    scrollableAreas.forEach(container => {
        updateScrollArrows(container);
        updateCardCentering(container);
        container.addEventListener('scroll', () => updateScrollArrows(container));
        window.addEventListener('resize', () => {
            updateScrollArrows(container);
            updateCardCentering(container);
        });
    });
});
