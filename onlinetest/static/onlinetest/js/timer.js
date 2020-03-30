// variables
var countdown = document.getElementById("countdown");
var timer;
var specs = {
    'radius': 40,
    'centerX': 40,
    'centerY': 40,
    'thickness': 7,
    'offset': -Math.PI / 2,
    'color': '#FF8C00',
    'bgColor': 'black',
    'idFont': 'small-caps 400 1rem Molle',
    'valueFont': 'bold 1.5rem Molle',
    'fontColor': '#FF8C00',
};
var time = {
    'millisecond': 1000,
    'second': 60,
    'minute': 60,
    'hour': 24,
}
var info = {};


// canvas init
var canvasElements = Array.prototype.slice.call(document.querySelectorAll('canvas'));
var canvasCtx = [];
canvasElements.forEach(function (canvas, index) {
    canvas.width = specs.centerX * 2;
    canvas.height = specs.centerY * 2;
    canvasCtx[index] = canvas.getContext('2d');
    var name = canvas.id;
    info[name] = { 'ctx': index, 'value': 0, 'prevValue': -1 };
});
var canvasKeys = Object.keys(info);
// info.hours.denominator = time.hour;
info.minutes.denominator = time.minute;
info.seconds.denominator = time.second;


// show remaining time
function showRemainingTime() {
    // calculate new values
    var secondsLeft = init_time;
    init_time -= 1;
    if(init_time < 0){
        init_time = 0;
    }
    // info.minutes.value = Math.floor((secondsLeft % (time.second * time.minute)) / time.second);
    info.minutes.value = Math.floor(secondsLeft / time.second);
    info.seconds.value = Math.floor(secondsLeft % time.second);

    // update changed values only
    canvasKeys.forEach(function (key) {
        if (info[key].value !== info[key].prevValue) {
            draw(canvasCtx[info[key].ctx], info[key].value / info[key].denominator, key, info[key].value);
            info[key].prevValue = info[key].value;
        }
    });
}

// draw function
function draw(ctx, part, id, value) {
    // calculate angles
    var start = specs.offset;
    var between = 2 * Math.PI * part + specs.offset;
    var end = 2 * Math.PI + specs.offset;

    // clear canvas
    ctx.clearRect(0, 0, specs.centerX * 2, specs.centerY * 2);

    // draw remaining %
    ctx.fillStyle = specs.color;
    ctx.beginPath();
    ctx.arc(specs.centerX, specs.centerY, specs.radius, start, between);
    ctx.arc(specs.centerX, specs.centerY, specs.radius - specs.thickness, between, start, true);
    ctx.closePath();
    ctx.fill();

    // draw bg
    ctx.fillStyle = specs.bgColor;
    ctx.beginPath();
    ctx.arc(specs.centerX, specs.centerY, specs.radius, between, end);
    ctx.arc(specs.centerX, specs.centerY, specs.radius - specs.thickness, end, between, true);
    ctx.closePath();
    ctx.fill();

    // draw text
    ctx.fillStyle = specs.fontColor;
    ctx.font = specs.idFont;
    ctx.fillText(id, specs.radius - ctx.measureText(id).width / 2, (specs.thickness+3) * 3);
    ctx.font = specs.valueFont;
    ctx.fillText(value, specs.radius - ctx.measureText(value).width / 2, specs.radius * 2 - specs.thickness * 3);
}

function startTimer(){
    // change countdown every second
    timer = setInterval(showRemainingTime, 1000);
}
