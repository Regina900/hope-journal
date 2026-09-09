// ============================================================
// HOPE JOURNAL
// Main JavaScript
// ============================================================


// ============================================================
// PAGE READY
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Hope Journal loaded successfully 🌿");


    // --------------------------------------------------------
    // AUTO-HIDE FLASH MESSAGES
    // --------------------------------------------------------

    const flashMessages =
        document.querySelectorAll(".flash-message");


    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";

            message.style.transform =
                "translateY(-5px)";


            setTimeout(function () {

                message.remove();

            }, 300);

        }, 5000);

    });


    // --------------------------------------------------------
    // CONFIRM LOGOUT
    // --------------------------------------------------------

    const logoutLinks =
        document.querySelectorAll(".logout");


    logoutLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to log out?"
            );


            if (!confirmed) {

                event.preventDefault();

            }

        });

    });


    // --------------------------------------------------------
    // TEXTAREA CHARACTER COUNTER
    // --------------------------------------------------------

    const textareas =
        document.querySelectorAll("textarea");


    textareas.forEach(function (textarea) {

        const maxLength = 5000;


        // Create counter

        const counter =
            document.createElement("div");


        counter.className =
            "character-counter";


        counter.textContent =
            `0 / ${maxLength}`;


        textarea.insertAdjacentElement(
            "afterend",
            counter
        );


        function updateCounter() {

            const length =
                textarea.value.length;


            counter.textContent =
                `${length} / ${maxLength}`;


            if (length > 4500) {

                counter.classList.add(
                    "warning"
                );

            } else {

                counter.classList.remove(
                    "warning"
                );

            }

        }


        textarea.addEventListener(
            "input",
            updateCounter
        );


        updateCounter();

    });


    // --------------------------------------------------------
    // PREVENT EMPTY JOURNAL SUBMISSION
    // --------------------------------------------------------

    const journalForms =
        document.querySelectorAll(
            'form[action*="journal"]'
        );


    journalForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const textarea =
                    form.querySelector("textarea");


                if (!textarea) {

                    return;

                }


                const content =
                    textarea.value.trim();


                if (!content) {

                    event.preventDefault();


                    alert(
                        "Please write something before saving your journal entry."
                    );


                    textarea.focus();

                }

            }
        );

    });


    // --------------------------------------------------------
    // BUTTON LOADING STATE
    // --------------------------------------------------------

    const forms =
        document.querySelectorAll("form");


    forms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function () {

                const submitButton =
                    form.querySelector(
                        'button[type="submit"], input[type="submit"]'
                    );


                if (!submitButton) {

                    return;

                }


                setTimeout(function () {

                    submitButton.disabled = true;

                    submitButton.style.opacity =
                        "0.7";


                    if (
                        submitButton.tagName ===
                        "BUTTON"
                    ) {

                        submitButton.textContent =
                            "Saving...";

                    }

                }, 50);

            }
        );

    });


    // --------------------------------------------------------
    // SMOOTH SCROLL
    // --------------------------------------------------------

    const smoothLinks =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    smoothLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const targetId =
                    link.getAttribute("href");


                if (
                    !targetId ||
                    targetId === "#"
                ) {

                    return;

                }


                const target =
                    document.querySelector(
                        targetId
                    );


                if (target) {

                    event.preventDefault();


                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }

            }
        );

    });

});