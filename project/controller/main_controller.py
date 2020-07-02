from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from project.model.service.baby_monitor_service import BabyMonitorService
from flask import render_template
from flask_socketio import emit
from project import app, socketio
from time import sleep
from project.util.clean_dict import clean_dict_baby_monitor
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from project.model.publisher.smart_tv_publisher import SmartTvPublisher
from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.service.smart_tv_service import SmartTvService
from project.model.smartphone import confirm_user, control, mutex_confirm
from project.model.smart_tv import block
# from project.util.wait_user_confirm import checkUserConfirm


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


bm_on = False
sp_on = False
tv_on = False


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


@socketio.on("babymonitorDesconnect")
def babymonitor_desconnect():
    global bm_on
    bm_on = False


@socketio.on("smartphoneConnect")
def smartphone_connect():
    global sp_on
    sp_on = True
    info = {"info": "Smartphone Start"}
    socketio.emit("SmartphoneInformation", info)
    # check_user_confirm = checkUserConfirm()
    subscriber_bm = SmartphoneSubscriber("babymonitor")
    subscriber_tv = SmartphoneSubscriber("smart_tv")
    subscriber_bm.start()
    subscriber_tv.start()
    # check_user_confirm.start()
    while True:
        sleep(1)
        if not sp_on:
            subscriber_bm.stop()
            subscriber_tv.stop()
            # check_user_confirm.stop()
            break


@socketio.on("smartphoneDesconnect")
def smartphone_desconnect():
    global sp_on
    sp_on = False


@socketio.on("tvConnect")
def tv_connect():
    global tv_on
    tv_on = True
    subscriber = SmartTvSubscriber()
    subscriber.start()
    while True:
        sleep(1)
        if not tv_on:
            subscriber.stop()
            break


@socketio.on("tvDesconnect")
def tv_desconnect():
    global tv_on
    tv_on = False


@socketio.on("confirmUser")
def user_confirm():
    SmartphonePublisher("confirmation").start()

    last_record = BabyMonitorService(BabyMonitorSend).last_record()
    user_confirm = {"id_notification": last_record["id"], "type": "confirm"}
    BabyMonitorService(BabyMonitorReceive).insert_data(user_confirm)


@socketio.on("tvBlocked")
def blocked_tv(blocked):
    if blocked:
        info = {"info": "Tv blcoked"}
        socketio.emit("TvInformation", info)
        socketio.emit("RedColor")
        SmartTvService().insert_data(dict(block=True))
    else:
        info = {"info": "Tv available"}
        socketio.emit("TvInformation", info)
        socketio.emit("NormalColor")
        SmartTvService().insert_data(dict(block=False))
