# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
from project import app, socketio

if __name__ == "__main__":
    print('Run BabyMonitorSoS \n')
    socketio.run(app)
