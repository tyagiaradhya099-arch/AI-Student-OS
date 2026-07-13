const calendar = document.getElementById("dashboardCalendar");
const monthText = document.getElementById("dashboardMonth");

const prevBtn = document.getElementById("prevDashboardMonth");
const nextBtn = document.getElementById("nextDashboardMonth");

let currentDate = new Date();

const months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
];

function renderCalendar(){

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthText.textContent = `${months[month]} ${year}`;

    calendar.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    // Empty spaces
    for(let i = 0; i < firstDay; i++){

        const empty = document.createElement("span");
        calendar.appendChild(empty);

    }

    const today = new Date();

    // Days
    for(let day = 1; day <= lastDate; day++){

        const span = document.createElement("span");

        span.textContent = day;

        if(
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ){
            span.classList.add("active-day");
        }

        calendar.appendChild(span);

    }

}

prevBtn.addEventListener("click",function(){

    currentDate.setMonth(currentDate.getMonth()-1);

    renderCalendar();

});

nextBtn.addEventListener("click",function(){

    currentDate.setMonth(currentDate.getMonth()+1);

    renderCalendar();

});

renderCalendar();