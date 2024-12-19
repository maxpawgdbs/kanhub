document.addEventListener("DOMContentLoaded", function () {
    let currentDate = new Date();

    const urlParams = new URLSearchParams(window.location.search);
    const dateParam = urlParams.get('date');
    if (dateParam) {
    currentDate = new Date(dateParam);
    }

    function updateMonthYearDisplay() {
    const monthYearElement = document.getElementById("month-year");
    const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
    monthYearElement.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
    }

    function updateDateParamInUrl() {
    const newDate = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-01`;
    const url = new URL(window.location.href);
    url.searchParams.set('date', newDate);
    window.location.href = url.toString();
    }

    document.getElementById("prev-month").addEventListener("click", function () {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateMonthYearDisplay();
    updateDateParamInUrl();
    });

    document.getElementById("next-month").addEventListener("click", function () {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateMonthYearDisplay();
    updateDateParamInUrl();
    });

    updateMonthYearDisplay();
});
