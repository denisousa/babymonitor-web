from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import exchange, queue_smartphone, bm_info
from project.model.business.smartphone_business import (
    wait_user_confirm,
    check_is_notification,
    send_confirm_baby_monitor,
    forward_message_smart_tv,
    type_notification,
)
from project.model.smartphone import control, confirm_user, mutex_confirm
from project import socketio
from flask_socketio import emit
from threading import Thread
import json
from time import sleep


data = None

class SmartphoneSubscriber(ConfigScenario, Thread):
    def __init__(self, type_consume):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.type_consume = type_consume
        self.declare_exchange(exchange, "direct")
        self.declare_queue(queue_smartphone)
        self.bind_exchange_queue(exchange, queue_smartphone, bm_info)

    def run(self):
        if self.type_consume == "babymonitor":
            self.consume_message_baby_monitor()
        if self.type_consume == "smart_tv":
            self.consume_message_tv()

    def stop(self):
        if self.type_consume == 'babymonitor':
            print("(Subscribe) SP|BM: Close")
        else:
            print("(Subscribe) SP|TV: Close")

    def consume_message_baby_monitor(self):
        print(
            " [*] Smartphone waiting for messages from Baby Monitor. To exit press CTRL+C"
        )
        self.channel.basic_consume(
            queue=queue_smartphone,
            on_message_callback=self.callback_babymonitor_sm,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def consume_message_tv(self):
        print(" [*] Smartphone waiting for messages from TV. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smartphone,
            on_message_callback=self.callback_smart_tv,
            auto_ack=True,
        )

        self.channel.start_consuming()
        socketio.emit(
            "SmartphoneReceive", {"msg": "ISSO VAI FUNCIONAR DEMAIS CARAAAAAAAAA"}
        )
        self.channel.start_consuming()

    def callback_babymonitor_sm(self, ch, method, properties, body):
        global control
        global confirm_user, mutex_confirm

        body = body.decode("UTF-8")
        body = json.loads(body)
        notification = check_is_notification(body)
        socketio.emit("SmartphoneReceive", body)
        if notification:
            info = type_notification(body)
            socketio.emit("SmartphoneInformation", {"info": info})
            if control:
                control = False
                thread_wait_user = Thread(target=wait_user_confirm, args=(body,))
                thread_wait_user.start()
            if confirm_user:
                send_confirm_baby_monitor()
                socketio.emit("SmartphoneSent", {"info": "Confirmation Sent to BabyMonitor!"})
                mutex_confirm.acquire()
                confirm_user = False
                mutex_confirm.release()
        else:
            mutex_confirm.acquire()
            control = True
            mutex_confirm.release()
            socketio.emit("SmartphoneInformation", {"info": "Emma is fine."})

    def callback_smart_tv(self, ch, method, properties, body):
        pass
