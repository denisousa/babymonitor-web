from project.model.smartphone import Smartphone
from app import db


class SmartphoneService():
    def insert_data(self):
        status_baby = Smartphone(False , False, True, 0)
        db.session.add(status_baby)
        db.session.commit()

    def return_data(self):
        return Smartphone.query.order_by(Smartphone.id.desc()).first()
