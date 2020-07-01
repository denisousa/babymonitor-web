from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber


class SmartphoneController():
    def start_publisher(self):
        publisher = SmartphonePublisher()
        publisher.start()
        publisher.join()

    def start_subscriber(self):
        subscriber = SmartphoneSubscriber('babymonitor')
        subscriber.start()
        subscriber.join()
