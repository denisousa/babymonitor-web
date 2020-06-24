from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import make_config
from flask_cors import CORS
from flask_babel import Babel


app = Flask(__name__)
make_config(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
babel = Babel(app)
CORS(app)

from .util import (
    body_message,
    config_broker,
    connection_broker,
    construct_scenario,
)
from .controller import main_controller
from .model import baby_monitor, smartphone, smart_tv

db.create_all()
from .util import start_subscribers
