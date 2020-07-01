from project import db
from project.model.baby_monitor import BabyMonitorSend
from datetime import datetime


class BabyMonitorService:
    def __init__(self, database):
        self.database = database

    def insert_data(self, data):
        data_babymonitor = self.database(**data, time=datetime.utcnow())
        db.session.add(data_babymonitor)
        db.session.commit()

    def update_data(self, data):
        last_record = self.database().query.order_by(self.database.id.desc()).first()
        if data["crying"]:
            crying = {"crying": data["crying"]}
            BabyMonitorSend.query.filter_by(id=last_record.id).update(crying)
        if not data["breathing"]:
            time_no_breathing = {"time_no_breathing": data["time_no_breathing"]}
            BabyMonitorSend.query.filter_by(
                id=last_record.id).update(time_no_breathing)
        db.session.commit()

    def last_record(self):
        data = self.database().query.order_by(
            self.database.id.desc()).first()
        if not data:
            return data

        return data.__dict__
