var disconnect_sm = false;
var data_sm = false;


document.querySelector('#btn-smartphone').onclick = function () {
    data_sm = !data_sm
    if(data_sm) {
        socket.emit('smartphone', { msg : 'start' });
        disconnect_sm = false;
    } else {
        disconnect_sm = true;
    }
};


socket.on('updateSmartphone', function(msg) {
    if (!disconnect_sm) {
        var breathing = 'Breathing: ' + msg['body'];
        var sleeping = 'Sleeping: ' + msg['body'];
        var timeNoBreathing = 'Time no Breathing: ' + msg['body'];
        document.querySelector("#smartphone-data .breathing").innerHTML = breathing;
        document.querySelector("#smartphone-data .sleeping").innerHTML = sleeping;
        document.querySelector("#smartphone-data .time-no-breathing").innerHTML = timeNoBreathing;
        socket.emit('smartphone', { msg : 'start' });
    } else {
        document.querySelector("#smartphone-data .breathing").innerHTML = 'Breathing: ';
        document.querySelector("#smartphone-data .sleeping").innerHTML = 'Sleeping: ';
        document.querySelector("#smartphone-data .time-no-breathing").innerHTML = 'Time no Breathing: ';
    }
});
