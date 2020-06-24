from project import db


class BabyMonitor(db.Model):
    __tablename__ = "baby_monitor"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    block = db.Column(db.Boolean, nullable=False)
    crying = db.Column(db.Boolean, nullable=False)
    sleeping = db.Column(db.Boolean, nullable=False)
    breathing = db.Column(db.Boolean, nullable=False)
    time_no_breathing = db.Column(db.Integer, nullable=False)
