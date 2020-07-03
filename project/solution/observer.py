import pika
import threading
import json
from time import sleep
from pyrabbit.api import Client
from project.solution.observer_service import ObserverService
from project.solution.observer_model import ObserverModel


class Observer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.queue = "observer"
        self.channel.queue_declare(self.queue)
        self.bindings = self.subscribe_in_all_queues()
        self.notification = False
        self.adaptation = False
        self.block_tv = None

    def get_bindings(self):
        client = Client("localhost:15672", "guest", "guest")
        bindings = client.get_bindings()
        bindings_result = []

        for b in bindings:
            if b["source"] == "exchange_baby_monitor":
                bindings_result.append(b)

        print('BINDINGS: ', bindings_result)
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

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(
            " [OBSERVER] Receive Topic: %r | Message: %r" % (method.routing_key, body)
        )
        body = json.loads(body.decode("UTF-8"))
        self.read_message(body, method.routing_key)

    def run(self):
        print("Working Observer")
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        raise SystemExit()

    def read_message(self, message, source):
        if message["type"] == "notification":
            print("OBSERVER - Recebi mensagem de notificação")
            if self.adaptation:
                print("OBSERVER - Minha adaptação falhou")
                ObserverService(ObserverModel).insert_data({"success": False})
            self.notification = True

        if message["type"] == "confirmation":
            if self.adaptation:
                print("OBSERVER - Minha adaptação deu certo")
                ObserverService(ObserverModel).insert_data({"success": True})
                self.adaptation = False
            self.notification = False

        if message["type"] == "status" and source == "st_info":
            if message["block"]:
                print("OBSERVER -Vou desbloquear a TV")
                self.adaptation = True
                self.adapt_tv()

    def adapt_tv(self):
        self.block_tv(False)
        sleep(2)

# Confirmação -> Usuário ou da TV
# Se recebe notificação
# 1 - Conexão ao broker
# 2 - Cria fila só para ele e escuta de todas as rotas
# 3 - Se ele recebe msg da TV dizendo que está bloqueada
