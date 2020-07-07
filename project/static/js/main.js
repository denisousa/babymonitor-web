var socket = io.connect('http://localhost:5000');
var disconnect_bm = false;
var data_bm = false;

document.querySelector('#btn-babymonitor').onclick = function () {
    data_bm = !data_bm
    if (data_bm) {
        socket.emit('babymonitorConnect');
        document.querySelector('#btn-babymonitor').innerHTML = 'Stop';
        disconnect_bm = false;
        changeColor("#17a2b8", "white", ".bm");
        setTimeout(function () {
            changeColor("white", "black", ".bm");
        }, 1000);
    } else {
        disconnect_bm = true;
        socket.emit('babymonitorDisconnect');
        document.querySelector('#btn-babymonitor').innerHTML = 'Start';
        changeColor("#CD5C5C", "white", ".bm")
        setTimeout(function () {
            changeColor("white", "black", ".bm")
            document.querySelector("#babymonitor-sent").innerHTML = '';
            document.querySelector("#babymonitor-receive").innerHTML = '';
            document.querySelector("#babymonitor-information").innerHTML = '';
        }, 1000);
    }
};

socket.on('BabyMonitorSent', function (msg) {
    document.querySelector("#babymonitor-sent").innerHTML = '';
    if (!disconnect_bm) {
        console.log('HEREEEEEEE');
        console.log(msg);
        var type = msg['type'];
        var breathing = 'Breathing: ' + msg['breathing'];
        var sleeping = 'Sleeping: ' + msg['sleeping'];
        var crying = 'Crying: ' + msg['crying'];
        var timeNoBreathing = 'Time no Breathing: ' + msg['time_no_breathing'];
        document.querySelector(".babymonitor-sent type").innerHTML = type;
        document.querySelector(".babymonitor-sent breathing").innerHTML = breathing;
        document.querySelector(".babymonitor-sent crying").innerHTML = crying;
        document.querySelector(".babymonitor-sent sleeping").innerHTML = sleeping;
        document.querySelector(".babymonitor-sent time-no-breathing").innerHTML = timeNoBreathing;
    } else {
        document.querySelector(".babymonitor-sent type").innerHTML = '';
        document.querySelector(".babymonitor-sent breathing").innerHTML = '';
        document.querySelector(".babymonitor-sent sleeping").innerHTML = '';
        document.querySelector(".babymonitor-sent time-no-breathing").innerHTML = '';
        document.querySelector(".babymonitor-sent crying").innerHTML = '';
    }   
});

socket.on('BabyMonitorReceive', function (msg) {
    document.querySelector("#babymonitor-receive").innerHTML = '';
    if (!disconnect_bm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-receive").appendChild(p);
            setTimeout(function () {
                document.querySelector("#babymonitor-receive").innerHTML = '';
                document.querySelector("#tv-sent").innerHTML = '';
                document.querySelector("#tv-receive").innerHTML = '';
                document.querySelector("#tv-information").innerHTML = '';
                document.querySelector(".from-tv").innerHTML = '';
                document.querySelector("#smartphone-sent").innerHTML = '';
                document.querySelector("#smartphone-information").innerHTML = '';
                document.querySelector("#from-tv-information").innerHTML = ''; 
            }, 1000);
        }
    } else {
        document.querySelector("#babymonitor-receive").innerHTML = '';
    }
});

socket.on('successAdapter', function (msg) {
    changeColor("#148F77", "white", "#block");
});

// document.querySelector('#restart').onclick = function () {
//    socket.emit('restart');
// };