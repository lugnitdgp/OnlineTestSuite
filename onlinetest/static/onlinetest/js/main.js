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
}

var utimer;

//this should be called only when page loads
function start_timer_updater(init_time) {
    sleep(5000);// needs fix, async sleep required
    if(itime > 0){
        utimer = setInterval(update_time, 5000);
        // utimer = setInterval(function () { update_time(t_left); }, 5000);
    }
}