var disconnect_tv = false;
var block_tv = false;
var data_tv = false;


document.querySelector('#btn-tv').onclick = function () {
    data_tv = !data_tv
    if (data_tv) {
        socket.emit('tvConnect');
        disconnect_tv = false;
    } else {
        disconnect_tv = true;
        socket.emit('tvDisconnect');
    }
};

document.querySelector('#btn-tv-blocked').onclick = function () {
    block_tv = !block_tv;
    if (block_tv) {
        socket.emit('tvBlocked', true);
    } else {
        socket.emit('tvBlocked', false);
    }
};

socket.on('TvReceive', function (msg) {
    document.querySelector("#tv-receive").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#tv-receive").appendChild(p);
            setTimeout(function () {
                document.querySelector("#tv-receive").innerHTML = '';
            }, 3000);
        }
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
            setTimeout(function () {
                document.querySelector("#tv-information").innerHTML = '';
            }, 3000);
        }
    }
});

socket.on('RedColor', function (msg) {
    document.querySelector("#tv-color").style.backgroundColor = "#CD3333";
    document.querySelector("#tv-color").style.color = "#ffff";
});

socket.on('NormalColor', function (msg) {
    document.querySelector("#tv-color").style.backgroundColor = "white";
    document.querySelector("#tv-color").style.color = "black";
});
