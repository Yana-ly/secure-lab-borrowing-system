document.addEventListener("DOMContentLoaded", function () {
    var searchInputs = document.querySelectorAll("[data-table-search]");

    searchInputs.forEach(function (input) {
        var table = document.querySelector(input.getAttribute("data-table-search"));
        if (!table) return;

        input.addEventListener("input", function () {
            var term = input.value.toLowerCase();
            var rows = table.querySelectorAll("tbody tr");

            rows.forEach(function (row) {
                var rowText = row.textContent.toLowerCase();
                row.classList.toggle("d-none", term && !rowText.includes(term));
            });
        });
    });

    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", function () {
            var overlay = document.querySelector("[data-loading-overlay]");
            if (overlay) overlay.classList.add("show");
        });
    });
});
