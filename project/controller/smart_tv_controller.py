from project.model.publisher.smart_tv_publisher import SmartTvPublisher
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber


class SmartTvController():
    # subscriber = SmartTvSubscriber()
    # subscriber.start()
    # subscriber.join()

    publisher = SmartTvPublisher()
    publisher.start()
    publisher.join()