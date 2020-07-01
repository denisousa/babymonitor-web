from project.model.publisher.smartphone_publisher import SmartphonePublisher
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend, BabyMonitorReceive
from time import sleep
from datetime import datetime


user_confirm = None


def check_is_notification(message):
    print('TYPEEEE', message)
    if message["type"] == "notification":
        return True
    return False


def forward_message_smart_tv(notification):
    SmartphonePublisher("notification", notification).start()


def send_confirm_baby_monitor():
    SmartphonePublisher("confirmation").start()


def check_user_confirm():
    global user_confirm
    data_send = BabyMonitorService(BabyMonitorSend).last_record()
    data_receive = BabyMonitorService(BabyMonitorReceive).last_record()
    if data_receive:
        if data_receive["id_notification"] == data_send["id"]:
            return True

    return False


# pega o horário da primeira notificação
def wait_user_confirm():
    global user_confirm

    data_send = BabyMonitorService(BabyMonitorSend).last_record()
    if data_send and not user_confirm:
        user_confirm = data_send["time"]
    if user_confirm:
        delta_time = (datetime.utcnow() - user_confirm).total_seconds()
        print('\n\n\nHEEREEEE')
        print(check_user_confirm())
        print(delta_time)
    if not check_user_confirm() and delta_time > 5:
        user_confirm = None
        return False

    user_confirm = None
    return True


def type_notification(body):
    if body:
        if not body["breathing"]:
            return (
                f"Emma hasn't been breathing for {body['time_no_breathing']} seconds."
            )

        elif body["crying"]:
            return "Emma is crying."
