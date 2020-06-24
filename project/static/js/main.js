var socket = io.connect('http://localhost:5000');
var disconnect_bm = false;
var data_bm = false;


document.querySelector('#btn-babymonitor').onclick = function () {
    data_bm = !data_bm
    if(data_bm) {
        socket.emit('babymonitor', { msg : 'start', init: 'true' });
        disconnect_bm = false;
    } else {
        disconnect_bm = true;
    }
};


socket.on('updateBabymonitor', function(msg) {
    if (!disconnect_bm) {
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
    }
});

