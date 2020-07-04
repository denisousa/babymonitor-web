from project import socketio
from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from time import sleep

bm_on = False


@socketio.on("babymonitorConnect")
def babymonitor_connect():
    global bm_on
    bm_on = True
    info = {"info": "Baby Monitor Start"}
    socketio.emit("BabyMonitorInformation", info)
    subscriber = BabyMonitorSubscriber()
    subscriber.start()
    while True:
        sleep(1)
        if bm_on:
            publisher = BabyMonitorPublisher()
            publisher.start()
        else:
            subscriber.stop()
            break


@socketio.on("babymonitorDisconnect")
def babymonitor_disconnect():
    global bm_on
    bm_on = False
