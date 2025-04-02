
function toggleMenu() {
    const menu = document.getElementById('darkMenu');
    menu.classList.toggle('active');
    document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
}
function updateDescription(index) {
    const slides = document.querySelectorAll('.swiper-slide');
    const descriptionElement = document.getElementById('testimonial-description');
    descriptionElement.textContent = slides[index].getAttribute('data-description');
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
        const eventDay = `<br>This trip will begin in ${days} days,<br> ${hours} hours, ${minutes} minutes, and ${seconds}<br> seconds. Please check back later.`;
        
        const detailsElement = element.parentElement.querySelector('.countdown-details');
        if (detailsElement) {
            detailsElement.innerHTML = eventDay;
        }

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
            rotate: 0, // Prevents default rotation on Y
            stretch: 0,
            depth: 200,
            modifier: 1,
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
        },
        
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
        selectedFlag.src = `/static/flags/${countryCode}.gif`;
        selectedFlag.alt = `${selectedOption.text} Flag`;

        // Update dial code
        dialCode.textContent = `+${dialCodeValue}`;
    });
});
$(document).ready(function () {
    $("#openLoginPopupFromRegister").on("click", function (event) {
        event.stopPropagation(); // Prevent click from bubbling up
        $("#loginPopup").removeClass("hidden");
        $("#registerPopup").removeClass("active");
        setTimeout(() => {
            $("#loginForm [name='email']").focus();
        }, 100);
    });

    // Hide popup when clicking outside
    $(document).on("click", function (event) {
        if (!$(event.target).closest("#loginPopup, #openLoginPopupFromRegister").length) {
            $("#loginPopup").addClass("hidden");
        }
    });
});


$(document).ready(function () {
    $("#registerForm").submit(function (event) {
        event.preventDefault();
        event.stopPropagation(); // Prevents the form from submitting normally

        const formData = new FormData(this); // Collects the form data in the correct format

        const $signupBtn = $("#submitBtn");
        $signupBtn.prop("disabled", true).html('Continue <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: "/user/sign-up/",
            type: "POST",
            data: formData,
            processData: false, // Prevents jQuery from converting the FormData object to a string
            contentType: false, // Allows the FormData object to set its own content type
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (response) {
                if (response.success) {
                    console.log("Sign up successful!");
                    $("#registerPopup").addClass("hidden");
                    $("#successPopup").removeClass("hidden");
                    window.location.href = response.redirect_url;
                } else {
                    console.error(response.errors?.email || response.message || "An error occurred.");
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON;
                console.error(response);
            },
            complete: function () {
                $signupBtn.prop("disabled", false).html('Continue');
            }
        });
    });
    $("#loginForm").submit(function (event) {
        event.preventDefault();
    
        const formData = new FormData(this); // Collects the form data in the correct format
    
        const $signinBtn = $("#loginSubmitBtn");
        $signinBtn.prop("disabled", true).html('Signing In <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
    
        const csrfToken = $('#loginForm input[name="csrfmiddlewaretoken"]').val();
    
        $.ajax({
            url: "/user/login/", // Replace with your sign-in endpoint
            type: "POST",
            data: formData,
            processData: false, // Prevents jQuery from converting the FormData object to a string
            contentType: false, // Allows the FormData object to set its own content type
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (response) {
                if (response.success) {
                    console.log("Sign in successful!");
                    window.location.href = response.redirect_url; // Redirect to the specified URL
                } else {
                    // Handle errors (e.g., invalid credentials)
                    console.error(response.message || "An error occurred.");
                    console.error(response.message || "An error occurred."); // Optional: Display a message to the user
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON;
                console.error(response?.message || "An error occurred.");
                console.error(response?.message || "An error occurred."); // Optional: Display a message to the user
            },
            complete: function () {
                $signinBtn.prop("disabled", false).html('Sign In');
            }
        });
    });
});
