document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert-dismissible");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (alert) {
                $(alert).alert("close");
            }
        }, 5000);
    });
});