var socket = io.connect('http://localhost:5000');
var disconnect_bm = false;
var data_bm = false;

document.querySelector('#btn-babymonitor').onclick = function () {
    data_bm = !data_bm
    if(data_bm) {
        socket.emit('babymonitorConnect');
        disconnect_bm = false;
        changeColor("#17a2b8", "white", ".bm")
        setTimeout(function(){
            changeColor("white", "black", ".bm")
        }, 1000);
    } else {
        disconnect_bm = true;
        socket.emit('babymonitorDisconnect');
        changeColor("#CD5C5C", "white", ".bm")
        setTimeout(function(){
            changeColor("white", "black", ".bm")
        }, 1000);
    }
};

socket.on('BabyMonitorSent', function(msg) {
    document.querySelector("#babymonitor-sent").innerHTML = '';
    if (!disconnect_bm) {
        for(data in msg){
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-sent").appendChild(p);
        }
    } else {
        document.querySelector("#babymonitor-sent").innerHTML = '';
    }
});

socket.on('BabyMonitorReceive', function(msg) {
    document.querySelector("#babymonitor-receive").innerHTML = '';
    if (!disconnect_bm) {
        for(data in msg){
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-receive").appendChild(p);
            setTimeout(function(){
                document.querySelector("#babymonitor-receive").innerHTML = '';
            }, 3000);
        }
    } else {
        document.querySelector("#babymonitor-receive").innerHTML = '';
    }
});

socket.on('successAdapter', function(msg) {
    changeColor("#148F77", "white", ".bm")
    setTimeout(function(){
        changeColor("white", "black", ".bm")
    }, 1000);
});

document.querySelector('#restart').onclick = function () {
    socket.emit('restart');
};