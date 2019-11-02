//timer upadters
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function update_time(){
    tleft -= 5;
    //tleft is global here
    if(tleft >= -4){
        console.log("Should update time");
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/update_time/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("time_left=" + tleft.toString());
    }
    else {
        window.location.replace("/finish/");
    }
}

var utimer;

//this should be called only when page loads
async function start_timer_updater(init_time) {
    //await sleep(5000);
    if(init_time > 0){
        utimer = setInterval(update_time, 5000);
    }
}