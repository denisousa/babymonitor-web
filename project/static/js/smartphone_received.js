var disconnect_sm = false;
var data_sm = false;


document.querySelector('#btn-smartphone').onclick = function () {
    data_sm = !data_sm
    if (data_sm) {
        socket.emit('smartphoneConnect');
        disconnect_sm = false;
    } else {
        disconnect_sm = true;
        socket.emit('smartphoneDesconnect');
    }
};


socket.on('SmartphoneReceive', function (msg) {
    document.querySelector("#smartphone-receive").innerHTML = '';
    if (!disconnect_sm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#smartphone-receive").appendChild(p);
        }
        //socket.emit('smartphone', null);
    } else {
        document.querySelector("#smartphone-receive").innerHTML = '';
    }
});

socket.on('SmartphoneInformation', function (msg) {
    document.querySelector("#smartphone-information").innerHTML = '';
    if (!disconnect_sm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#smartphone-information").appendChild(p);
        }
    } else {
        document.querySelector("#smartphone-information").innerHTML = '';
    }
});