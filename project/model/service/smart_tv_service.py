from project.model.smart_tv import SmartTv
from app import db


class SmartTvService():
    def insert_data(self):
        status_baby = SmartTv(False , False, True, 0)
        db.session.add(status_baby)
        db.session.commit()

    def return_data(self):
        return SmartTv.query.order_by(SmartTv.id.desc()).first()
