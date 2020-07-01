from project.util.construct_scenario import (
    exchange,
    bm_info,
    st_info,
)
from project.util.config_broker import ConfigScenario
from project.util.body_message import construct_message
from threading import Thread
from project import socketio
import json


class SmartphonePublisher(ConfigScenario, Thread):
    def __init__(self, type, notification=None):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "direct")
        self.type = type
        self.notification = notification

    def run(self):
        if self.type == "confirmation":
            self.publish_confirmation()
        if self.type == "notification":
            self.forward_message()

    def publish_confirmation(self):
        confirmation = json.dumps({"info": "Notification confirmed!"})

        self.channel.basic_publish(
            exchange=exchange, routing_key=bm_info, body=confirmation,
        )
        print("(Publish) SM|BM: ", confirmation)

    def forward_message(self):

        self.channel.basic_publish(
            exchange=exchange, routing_key=st_info, body=self.notification,
        )
        print("(Publish) SM|ST: ", self.notification)
