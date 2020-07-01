var socket = io.connect('http://localhost:5000');
var disconnect_bm = false;
var data_bm = false;


document.querySelector('#btn-babymonitor').onclick = function () {
    data_bm = !data_bm
    if(data_bm) {
        socket.emit('babymonitorConnect');
        disconnect_bm = false;
    } else {
        disconnect_bm = true;
        socket.emit('babymonitorDesconnect');
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
        // socket.emit('babymonitor', { msg : null });
    } else {
        document.querySelector("#babymonitor-sent").innerHTML = '';
    }
});

socket.on('BabyMonitorReceive', function(msg) {
    document.querySelector("#babymonitor-receive").innerHTML = '';
    if (!disconnect_sm) {
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
