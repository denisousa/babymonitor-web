from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from project.model.subscriber.baby_monitor_subscriber import (
    BabyMonitorSubscriber)
from project.model.baby_monitor import BabyMonitorSend
from project.model.service.baby_monitor_service import BabyMonitorService
from project.util.clean_dict import clean_dict_baby_monitor
from project import socketio


class BabyMonitorController():
    def start_publisher(self):
        publisher = BabyMonitorPublisher()
        publisher.start()

    def start_subscriber(self):
        subscriber = BabyMonitorSubscriber()
        subscriber.start()
