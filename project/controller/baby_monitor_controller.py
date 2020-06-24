from project.model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.service.baby_monitor_service import BabyMonitorService
from project.util.generate_data import data_from_baby


class BabyMonitorController():
    def start_publisher(self):
        # data = data_from_baby('force_fine')
        # BabyMonitorService().insert_data(data)
        publisher = BabyMonitorPublisher()
        publisher.start()
        publisher.join()

    def start_subscriber(self):
        subscriber = BabyMonitorSubscriber()
        subscriber.start()
        subscriber.join()

