function add_timer_element() {
    var elemDiv = document.createElement('div');
    elemDiv.style.cssText = 'position:fixed;width:100%;height:100%;opacity:0.3;z-index:100;background:#004;top:0;right:0;';
    document.body.appendChild(elemDiv);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function update_time(tleft){
    let tleft = parseInt(tleft);
    tleft -= 30;

    if(tleft >= -29){
        console.log("Should update time");
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "update_time/", true);
        xhttp.send("time_left="+tleft.toString());
    }
}

//this should be called only when page loads
function timer(init_time) {
    let itime = parseInt(init_time);
    await sleep(30000);//30sec
    var t_left = itime;
    if(itime > 0){
        setInterval(update_time(t_left), 30000);
    }
}