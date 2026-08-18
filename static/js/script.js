document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Auto-hide alerts

        const alerts = document.querySelectorAll(
            ".alert"
        );

        alerts.forEach(
            function (alert) {

                setTimeout(
                    function () {

                        const closeButton =
                            alert.querySelector(
                                ".btn-close"
                            );

                        if (closeButton) {
                            closeButton.click();
                        }

                    },
                    5000
                );

            }
        );


        // Confirm delete

        const deleteButtons =
            document.querySelectorAll(
                ".delete-confirm"
            );


        deleteButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function (event) {

                        const confirmed =
                            confirm(
                                "Are you sure you want to delete this application?"
                            );

                        if (!confirmed) {

                            event.preventDefault();

                        }

                    }
                );

            }
        );

    }
);