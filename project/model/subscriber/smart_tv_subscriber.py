from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import exchange, queue_smart_tv, st_msg
from project.model.business.smart_tv_business import check_available_tv
from project import socketio
from threading import Thread


class SmartTvSubscriber(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, "direct")
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
            queue=queue_smart_tv, on_message_callback=self.callback, auto_ack=True,
        )

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        available = check_available_tv()
        if available:
            # TODO Envia mensagem no tópico smart_tv_msg
            # informando alerta exibido. Não entendi by Denis
            info = {"info": "Tv is avaliable"}
            socketio.emit("TvInfomration", info)
            socketio.emit("TvReceive", body)
        else:
            # TODO Envia mensagem no tópico smart_tv_msg
            # informando que está bloqueada. Não entendi by Denis
            info = {"info": "Tv is blocked"}
            socketio.emit("TvInfomration", info)
