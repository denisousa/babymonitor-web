from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from project.model.service.baby_monitor_service import BabyMonitorService
from flask import render_template
from flask_socketio import emit
from project import app, socketio
from time import sleep
from project.util.clean_dict import clean_dict_baby_monitor
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.service.smart_tv_service import SmartTvService


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
    subscriber_bm = SmartphoneSubscriber("babymonitor")
    subscriber_tv = SmartphoneSubscriber("smart_tv")
    subscriber_bm.start()
    subscriber_tv.start()
    while True:
        sleep(1)
        if not sp_on:
            subscriber_bm.stop()
            subscriber_tv.stop()
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
    last_record = BabyMonitorService(BabyMonitorSend).last_record()
    user_confirm = {"id_notification": last_record["id"], "type": "confirm"}
    BabyMonitorService(BabyMonitorReceive).insert_data(user_confirm)
    SmartphonePublisher("confirmation").start()


@socketio.on("blockedTv")
def blocked_tv(blocked):
    if blocked:
        data = {"blocked": True}
    else:
        data = {"blocked": False}
    SmartTvService().insert_data(data)


"""@socketio.on("smartphone")
def smartphone_message(data):
    sleep(1)
    SmartphoneController().start_subscriber()
    #import ipdb; ipdb.set_trace()
    msg = clean_dict_baby_monitor(
        BabyMonitorService(BabyMonitorSend).last_record())
    if msg:
        if msg["type"] == "notification":

            message = ""
            if not msg["breathing"]:
                message = f"Emma hasn't been breathing for {msg['time_no_breathing']} seconds."

            elif msg["crying"]:
                message = "Emma is crying."

            emit("SmartphoneInformation", {"info": message})
        else:
            emit("SmartphoneInformation", {"info": "Emma is fine."})
    emit("SmartphoneReceive", msg)"""

