from project.model.baby_monitor import BabyMonitor
from project import db


class BabyMonitorService():
    def insert_data(self, data):
        babymonitor = BabyMonitor(block=False, **data)
        db.session.add(babymonitor)
        db.session.commit()

    def return_data(self):
        return BabyMonitor.query.order_by(BabyMonitor.id.desc()).first()
