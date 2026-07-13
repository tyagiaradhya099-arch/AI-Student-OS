const monthYear=document.getElementById("monthYear");
const calendarDays=document.getElementById("calendarDays");

const prevBtn=document.getElementById("prevMonth");
const nextBtn=document.getElementById("nextMonth");

let currentDate = new Date(2026,6);

function renderCalendar(){

    calendarDays.innerHTML="";

    const year=currentDate.getFullYear();

    const month=currentDate.getMonth();

    const firstDay=new Date(year,month,1).getDay();

    const lastDate=new Date(year,month+1,0).getDate();

    const months=[
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ];

    monthYear.innerText=`${months[month]} ${year}`;

    for(let i=0;i<firstDay;i++){

        const empty=document.createElement("div");

        empty.classList.add("empty");

        calendarDays.appendChild(empty);

    }

    const today=new Date();

    for(let d=1;d<=lastDate;d++){

        const day=document.createElement("div");

        day.classList.add("day");

        day.innerText=d;

        if(
            d===today.getDate() &&
            month===today.getMonth() &&
            year===today.getFullYear()
        ){
            day.classList.add("today");
        }

        calendarDays.appendChild(day);

    }

}

prevBtn.onclick=function(){

    currentDate.setMonth(currentDate.getMonth()-1);

    renderCalendar();

}

nextBtn.onclick=function(){

    currentDate.setMonth(currentDate.getMonth()+1);

    renderCalendar();

}

renderCalendar();