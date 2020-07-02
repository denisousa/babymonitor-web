from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import (
    exchange,
    queue_smartphone_bm,
    queue_smartphone_st,
    queue_smart_tv,
    bm_info,
    st_msg,
    st_info,
)
from project.model.business.smartphone_business import (
    wait_user_confirm,
    check_is_notification,
    send_confirm_baby_monitor,
    forward_message_smart_tv,
    type_notification,
)
from project.model.smartphone import control, confirm_user, mutex_confirm
from project import socketio
from threading import Thread
import threading
import json
from project.model.publisher.smartphone_publisher import SmartphonePublisher


data = None


class SmartphoneSubscriber(ConfigScenario, Thread):
    def __init__(self, type_consume):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self._stop = threading.Event()
        self.type_consume = type_consume
        self.declare_exchange(exchange, "direct")
        self.declare_queue(queue_smartphone_bm)
        self.declare_queue(queue_smartphone_st)

    def run(self):
        if self.type_consume == "babymonitor":
            self.bind_exchange_queue(exchange, queue_smartphone_bm, bm_info)
            self.consume_message_baby_monitor()
        if self.type_consume == "smart_tv":
            self.bind_exchange_queue(exchange, queue_smartphone_st, st_info)
            self.consume_message_tv()

    def stop(self):
        if self.type_consume == "babymonitor":
            print("(Subscribe) SP|BM: Close")
            self._stop.set()
            self._stop.isSet()
        else:
            print("(Subscribe) SP|TV: Close")
            self._stop.set()
            self._stop.isSet()

    def consume_message_baby_monitor(self):
        print(
            " [*] Smartphone waiting for messages from Baby Monitor. To exit press CTRL+C"
        )
        self.channel.basic_consume(
            queue=queue_smartphone_bm,
            on_message_callback=self.callback_babymonitor_sm,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def consume_message_tv(self):
        print(" [*] Smartphone waiting for messages from TV. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smartphone_st,
            on_message_callback=self.callback_smart_tv,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def callback_babymonitor_sm(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        notification = check_is_notification(body)
        socketio.emit("SmartphoneReceive", body)
        if notification:
            info = type_notification(body)
            socketio.emit("SmartphoneInformation", {"info": info})
            if body["time_no_breathing"] == 10:
                forward_message_smart_tv()
        else:
            socketio.emit("SmartphoneInformation", {"info": "Emma is fine."})

    def callback_smart_tv(self, ch, method, properties, body):
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )
        body = body.decode("UTF-8")
        body = json.loads(body)
        socketio.emit('SmartphoneReceive', body)
        if body['block']:
            socketio.emit(
                'SmartphoneInformation',
                {'info': 'TV couldn\'t show message'}
            )
            # forward again
            forward_message_smart_tv()
        else:
            socketio.emit(
                'SmartphoneInformation',
                {'info': 'TV just showed the message'}
            )
            # send confirmation to BM
            SmartphonePublisher('confirmation').start()
            print('Confirmado Denis! SMARPHONE FALANDO \n\n\n\n\n\n\n')