var disconnect_sm = false;
var data_sm = false;


document.querySelector('#btn-smartphone').onclick = function () {
    data_sm = !data_sm
    if (data_sm) {
        socket.emit('smartphoneConnect');
        disconnect_sm = false;
        changeColor("#17a2b8", "white", ".sm")
        setTimeout(function(){
            changeColor("white", "black", ".sm")
        }, 1000);
    } else {
        disconnect_sm = true;
        socket.emit('smartphoneDesconnect');
        changeColor("#CD5C5C", "white", ".sm")
        setTimeout(function(){
            changeColor("white", "black", ".sm")
        }, 1000);
    }
};


socket.on('SmartphoneReceive', function (msg) {
    document.querySelector(".smartphone-receive").innerHTML = '';
    if (!disconnect_sm) {
        for (data in msg) {
            if('breathing' in msg) {
                showData(".smartphone-receive from-bm")
                deleteMessage(".smartphone-receive from-bm", 1000)
            }
            else {
                showData(".smartphone-receive from-tv")
                deleteMessage(".smartphone-receive from-tv", 1000)
            }
            // var p = document.createElement("p");
            // var value = document.createTextNode(data + ": " + msg[data]);
            // p.appendChild(value);
            // document.querySelector(".smartphone-receive").appendChild(p);
        }
    } // else {
      //  setTimeout(function () {
      //     document.querySelector(".smartphone-receive").innerHTML = '';
      //  }, 1000);
      //}
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
        setTimeout(function () {
            document.querySelector(".smartphone-receive").innerHTML = '';
        }, 3000);
    }
});