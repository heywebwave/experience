
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
document.querySelector('.register-content').addEventListener('click', function(event) {
    event.stopPropagation();
});


function toggleEvent() {
    const popup = document.getElementById('eventPopup');
    popup.classList.toggle('active');
    document.body.style.overflow = popup.classList.contains('active') ? 'hidden' : '';
}

// Update the click outside handler
document.addEventListener('click', function(event) {
    const popup = document.getElementById('eventPopup');
    const isClickInside = popup.contains(event.target);
    const isJoinUsButton = event.target.closest('.btn-dark');
    
    // Only handle click-outside on desktop
    if (window.innerWidth >= 992) {
        if (popup.classList.contains('active') && !isClickInside && !isJoinUsButton) {
            toggleEvent();
        }
    }
});
// Prevent popup from closing when clicking inside
document.querySelector('.event-content').addEventListener('click', function(event) {
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
        const dialCode = $("#dialCode").text().trim();
        const phoneNumberInput = $("input[name='phone_number']");
        let phoneNumber = phoneNumberInput.val().trim();


        // Prepend the dial code to the phone number if it's not already there
        if (!phoneNumber.startsWith(dialCode)) {
            phoneNumber = dialCode + phoneNumber;
            phoneNumberInput.val(phoneNumber);
            formData.set("phone_number", phoneNumber);
        }
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


$(document).ready(function () {
    $("#eventForm").submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(this); // Collects the form data in the correct format

        const $submitButton = $("#registrationButton");
        $submitButton.prop("disabled", true).html('Submitting <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

        const csrfToken = $('#eventForm input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: "/registration/", // Replace with your registration endpoint
            type: "POST",
            data: formData,
            processData: false, // Prevents jQuery from converting the FormData object to a string
            contentType: false, // Allows the FormData object to set its own content type
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (response) {
                if (response.success) {
                    console.log("Registration successful!");
                    $(this).reset(); // Reset the form
                    $submitButton.prop("disabled", true).html('Check your mailbox for payment');
                    // Optionally, you can reset the form here
                    $("hiddenPersonal").hide(); // Hide the button
                    $("#dietaryMedicalInfo").hide(); // Hide the button
                    $("#conferencePreferences").hide(); // Hide the button
                    $("#personalInfo").hide(); // Hide the button
    
                    // window.location.href = response.redirect_url; // Redirect to a thank-you page or homepage
                } else {
                    // Handle errors (e.g., validation errors)
                    console.error(response.errors || "An error occurred.");
                    $("#errorMessages").html(response.errors).removeClass("d-none"); // Show errors

                
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON;
                if (response && response.errors) {
                    // Display errors in the designated div
                    $("#errorMessages").html(response.errors).removeClass("d-none"); // Show errors
                } else {
                    console.error(response?.message || "An unexpected error occurred.");
                }
            },
            complete: function () {
                $submitButton.prop("disabled", false).html('Submit');

            }
        });
    });
});