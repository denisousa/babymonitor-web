import pika
import threading
import time
from pyrabbit.api import Client
from model.service.observer_service import ObserverService
from model.observer_model import ObserverModel
from controller.main_controller import blocked_tv


class Observer(threading.Thread):
    def __init__(self, is_adapted):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.queue = "observer"
        self.channel.queue_declare(self.queue)
        self.is_adapted = is_adapted
        self.notification = False
        self.adaptation = False

    def get_bindings(self):
        client = Client("localhost:15672", "guest", "guest")
        bindings = client.get_bindings()
        bindings_result = []

        for b in bindings:
            if b["source"] == "exchange_baby_monitor":
                bindings_result.append(b)

        return bindings_result

    def subscribe_in_all_queues(self):
        bindings = self.get_bindings()

        for bind in bindings:
            self.channel.queue_bind(
                exchange=bind["source"],
                queue=self.queue,
                routing_key=bind["routing_key"],
            )

        return bindings

    def run(self):
        def callback(ch, method, properties, body):
            print(
                " [OBSERVER] Receive Topic: %r | Message: %r"
                % (method.routing_key, body)
            )

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=True
        )

        self.channel.start_consuming()

    def read_message(self, message, source):
        if message["type"] == "notification":
            if self.adaptation:
                ObserverService(ObserverModel).insert_data({"success": False})
            self.notification = True

        if message["type"] == "confirmation":
            if self.adaptation:
                ObserverService(ObserverModel).insert_data({"success": True})
                self.adaptation = False
            self.notification = False

        if message["type"] == "status" and source == "st_info":
            if message["block"]:
                self.adaptation = True
                self.adapt_tv()

    def adapt_tv(self):
        blocked_tv(False)

    # def read_message(self, message, bindings):
    #     global semaphore, time_no_response, init, counttu
    #     if "NOTIFICATION" in message:
    #         count += 1
    #         if count == 1:
    #             init = time.time()
    #             time_no_response = 0
    #         else:
    #             time_no_response = time.time() - init

    #         print(f"* Time No response: {time_no_response} seconds.")
    #         if time_no_response >= 3:
    #             self.forward_message(message, bindings)

    #     if "STATUS" in message:
    #         semaphore.acquire()
    #         time_no_response = 0
    #         semaphore.release()

    # def forward_message(self, message, bindings):

    #     if smtv_controller.is_on():
    #         print("Status da tv: ", smtv_controller.get_status())

    #         if smtv_controller.get_status():
    #             self.publish_message(message, bindings)
    #         else:
    #             if self.is_adapted:
    #                 print("### Executing adaptation...")
    #                 print("Stopping application")
    #                 smtv_controller.stop_app()
    #                 self.publish_message(message, bindings)
    #                 # time.sleep(5)
    #                 """smtv_controller.start_app()
    #                 print('Reopening application')"""
    #             else:
    #                 print("### Unable to forward to TV...")
    #     else:
    #         print("### Unable to forward to TV...")

    # def publish_message(self, message, bindings):
    #     ex_rt = []

    #     for i in range(len(bindings)):
    #         if (
    #             "monitor" not in bindings[i]["destination"]
    #             and "smartphone" not in bindings[i]["destination"]
    #         ):
    #             ex_rt = [(bindings[i]["source"], bindings[i]["routing_key"])]

    #     for i in ex_rt:
    #         try:
    #             print("### Trying to send message to tv")
    #             self.channel.basic_publish(
    #                 exchange=i[0], routing_key=i[1], body=message
    #             )
    #             self.count = 0
    #             smp_controller.confirm_notification()
    #             print("### Sending confirmation to monitor")
    #             if self.is_adapted:
    #                 time.sleep(5)
    #                 smtv_controller.start_app()
    #                 print("Reopening application")
    #             return
    #         except Exception:
    #             print("Except publish...")
    #             pass


def main(is_adapted):
    global bindings

    thread_observer = Observer(is_adapted)
    bindings = thread_observer.subscribe_in_all_queues()
    thread_observer.start()


main(False)
# Confirmação -> Usuário ou da TV
# Se recebe notificação
# 1 - Conexão ao broker
# 2 - Cria fila só para ele e escuta de todas as rotas
# 3 - Se ele recebe msg da TV dizendo que está bloqueada
