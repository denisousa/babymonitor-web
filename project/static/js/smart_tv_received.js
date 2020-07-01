var disconnect_tv = false;
var data_tv = false;


document.querySelector('#btn-tv').onclick = function () {
    data_tv = !data_tv
    if (data_tv) {
        socket.emit('tvConnect');
        disconnect_tv = false;
    } else {
        disconnect_tv = true;
        socket.emit('tvDesconnect');
    }
};

document.querySelector('#btn-tv-blocked').onclick = function () {
    socket.emit('tvBlocked');
};

socket.on('TvReceive', function (msg) {
    document.querySelector("#tv-receive").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#tv-receive").appendChild(p);
        }
    } else {
        document.querySelector("#tv-receive").innerHTML = '';
    }
});

socket.on('TvInformation', function (msg) {
    document.querySelector("#tv-information").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#tv-information").appendChild(p);
        }
    } else {
        document.querySelector("#tv-information").innerHTML = '';
    }
});