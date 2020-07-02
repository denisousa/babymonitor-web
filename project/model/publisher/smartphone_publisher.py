from project.util.construct_scenario import (
    exchange,
    bm_msg,
    st_info,
    st_msg,
)
from project.util.config_broker import ConfigScenario
from project.model.service.baby_monitor_service import BabyMonitorSend
from project.model.service.baby_monitor_service import BabyMonitorService
from threading import Thread
from multiprocessing import Process
from project import socketio
import json
from project.util.clean_dict import clean_dict_baby_monitor
import pika


class SmartphonePublisher(ConfigScenario, Thread):
    def __init__(self, type):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "direct")
        self.type = type

    def run(self):
        if self.type == "confirmation":
            self.publish_confirmation()
        if self.type == "notification":
            self.forward_message()

    def publish_confirmation(self):
        confirmation = {"confirmation": "Notificaiton confirmed!"}

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=bm_msg,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps(confirmation),
        )
        socketio.emit("SmartphoneSent", confirmation)
        print("(Publish) SM|BM: ")

    def forward_message(self):
        notification = BabyMonitorService(BabyMonitorSend).last_record()
        notification = self.format_notification(notification)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=st_msg,
            properties=pika.BasicProperties(delivery_mode=2,),
            body=json.dumps({'notification': notification}),
        )
        socketio.emit("SmartphoneSent", {"notificaiton": notification})
        print("(Publish) SM|ST: ", notification)

    def format_notification(self, body):
        if body:
            if not body["breathing"]:
                return f"Emma hasn't been breathing for {body['time_no_breathing']} seconds."

            elif body["crying"]:
                return "Emma is crying."
