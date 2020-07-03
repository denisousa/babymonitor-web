from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import (
    exchange,
    queue_smart_tv,
    st_msg
)
from project import socketio
from threading import Thread
import json
from project.model.service.smart_tv_service import SmartTvService
from project.model.publisher.smart_tv_publisher import SmartTvPublisher


class SmartTvSubscriber(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "topic")
        self.declare_queue(queue_smart_tv)
        self.bind_exchange_queue(exchange, queue_smart_tv, st_msg)

    def run(self):
        self.consume_message()

    def stop(self):
        print("(Subscribe) TV: Close")
        raise SystemExit()

    def consume_message(self):
        print(" [*] Tv waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smart_tv,
            on_message_callback=self.callback,
            auto_ack=False
        )

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        socketio.emit("TvReceive", body)
        last_record = SmartTvService().last_record()

        if last_record is not None:
            # se não: Info -> "Notification: bla bla"
            # both: pub st_info -> 'I'm tananam'
            if not last_record['block']:
                socketio.emit("TvInformation", body)

            SmartTvPublisher().start()
