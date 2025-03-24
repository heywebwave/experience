
function toggleMenu() {
    const menu = document.getElementById('darkMenu');
    menu.classList.toggle('active');
    document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
}

// Intersection Observer for card animations
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        observer.observe(card);
    });
});

// Countdown Timer Function
function initCountdowns() {
    const countdowns = document.querySelectorAll('.countdown');
    
    function updateCountdown(element) {
        const targetDate = new Date(element.dataset.date);
        const now = new Date();
        const difference = targetDate - now;

        if (difference <= 0) {
            element.textContent = 'Event Started';
            return;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        // Format the countdown text
        element.textContent = `${days}d : ${hours}h : ${minutes}m : ${seconds}s`;

        // Add highlight animation when minutes or seconds change
        if (seconds === 0) {
            element.classList.add('highlight');
            setTimeout(() => element.classList.remove('highlight'), 1000);
        }
    }

    // Update all countdowns
    countdowns.forEach(countdown => {
        updateCountdown(countdown);
        setInterval(() => updateCountdown(countdown), 1000);
    });
}

// Initialize countdowns when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initCountdowns();
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper
    const testimonialSwiper = new Swiper('.testimonialSwiper', {
        effect: 'coverflow',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        initialSlide: 1,
        loop: true,
        loopedSlides: 3,
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2,
            slideShadows: false,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 3,
            }
        },
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        }
    });
});

function toggleRegister() {
    const popup = document.getElementById('registerPopup');
    popup.classList.toggle('active');
    document.body.style.overflow = popup.classList.contains('active') ? 'hidden' : '';
}

// Update the click outside handler
document.addEventListener('click', function(event) {
    const popup = document.getElementById('registerPopup');
    const isClickInside = popup.contains(event.target);
    const isJoinUsButton = event.target.closest('.btn-dark');
    
    // Only handle click-outside on desktop
    if (window.innerWidth >= 992) {
        if (popup.classList.contains('active') && !isClickInside && !isJoinUsButton) {
            toggleRegister();
        }
    }
});

// Prevent popup from closing when clicking inside
document.querySelector('.register-content').addEventListener('click', function(event) {
    event.stopPropagation();
});

// Country Select Handler
document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('countrySelect');
    const selectedFlag = document.getElementById('selectedFlag');
    const dialCode = document.getElementById('dialCode');

    countrySelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const countryCode = selectedOption.value.toLowerCase();
        const dialCodeValue = selectedOption.dataset.dialCode;

        // Update flag
        selectedFlag.src = `https://flagcdn.com/24x18/${countryCode}.png`;
        selectedFlag.alt = `${selectedOption.text} Flag`;

        // Update dial code
        dialCode.textContent = `+${dialCodeValue}`;
    });
});
