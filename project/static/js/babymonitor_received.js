socket.on('BabymonitorReceive', function(msg) {
    document.querySelector("#babymonitor-receive").innerHTML = '';
    if (!disconnect_sm) {
        for(data in msg){
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-receive").appendChild(p);
        }
        socket.emit('babymonitor', { msg : 'start' });
    } else {
        document.querySelector("#babymonitor-receive").innerHTML = '';
    }
});