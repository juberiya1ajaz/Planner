
function del() {
    alert("are you sure you want to proceed");
}

function changeBodyBg_dark() {

    document.body.style.color = "white"; // forecolor
    document.body.style.backgroundColor = "rgb(0,0,0,0.93)"; // backcolor
}
function changeBodyBg_light() {

    document.body.style.color = "black"; // forecolor
    document.body.style.backgroundColor = "white"; // backcolor
}
function printTable() {
    window.frames["print_frame"].document.body.innerHTML = document.getElementById("printTask").innerHTML;
    window.frames["print_frame"].window.focus();
    window.frames["print_frame"].window.print();
  }




