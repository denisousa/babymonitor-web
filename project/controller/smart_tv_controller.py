from project import socketio
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from project.model.publisher.smart_tv_publisher import SmartTvPublisher
from project.model.service.smart_tv_service import SmartTvService
from time import sleep


sp_on = False


@socketio.on("tvConnect")
def tv_connect():
    global tv_on
    tv_on = True
    subscriber = SmartTvSubscriber()
    SmartTvService().insert_data(dict(block=False))  # Setar aqui random
    subscriber.start()
    while True:
        sleep(1)
        if not tv_on:
            subscriber.stop()
            break


@socketio.on("tvDisconnect")
def tv_disconnect():
    global tv_on
    tv_on = False


@socketio.on("tvBlock")
def block_tv(blocked):
    if blocked:
        info = {"info": "Tv blocked"}
        socketio.emit("TvInformation", info)
        socketio.emit("RedColor")
        SmartTvService().insert_data(dict(block=True))
    else:
        info = {"info": "Tv available"}
        socketio.emit("TvInformation", info)
        socketio.emit("NormalColor")
        SmartTvService().insert_data(dict(block=False))
