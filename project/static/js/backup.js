var socket = io.connect('http://localhost:5000');
var disconnect = false;
var data = false;


document.querySelector('#btn-babymonitor').onclick = function () {
    data = !data
    // if(disconnect) {
    //     socket.connect();
    //     disconnect = false;
    // }
    if(data) {
        socket.emit('babymonitor', { msg : 'start' });
        disconnect = false;
    } else {
        disconnect = true;
    }
};

    
socket.on('updateBabymonitor', function(msg) {
    // var condition = Object.values(msg).includes("start");
    // console.log(msg);
    // console.log(condition);
    if (!disconnect) {
        var breathing = 'Breathing: ' + msg['body'];
        var sleeping = 'Sleeping: ' + msg['body'];
        var timeNoBreathing = 'Time no Breathing: ' + msg['body'];
        document.querySelector("#babymonitor-data .breathing").innerHTML = breathing;
        document.querySelector("#babymonitor-data .sleeping").innerHTML = sleeping;
        document.querySelector("#babymonitor-data .time-no-breathing").innerHTML = timeNoBreathing;
        socket.emit('babymonitor', { msg : 'start' });
    } else {
        document.querySelector("#babymonitor-data .breathing").innerHTML = 'Breathing: ';
        document.querySelector("#babymonitor-data .sleeping").innerHTML = 'Sleeping: ';
        document.querySelector("#babymonitor-data .time-no-breathing").innerHTML = 'Time no Breathing: ';
        // socket.disconnect();
        // disconnect = true;
    }
});