from project.controller.baby_monitor_controller import BabyMonitorController
from project.controller.smartphone_controller import SmartphoneController
from project.controller.smart_tv_controller import SmartTvController
from flask import render_template
from flask_socketio import emit
from project import app, socketio
import random
from time import sleep


args = {
    'tag': 'isso eh uma tag',
    'breathing': 'aaaa',
    'time_no_breathing': 'aaaa',
    'sleeping': '',
    'topic': 'aushaushau',
    'message': '',
    'x': '',
    'title': '',
}

@app.route('/', methods=['GET'])
def index():
    global args
    return render_template('index.html', args=args)


@socketio.on('babymonitor')
def handle_message(data):
    sleep(1)
    if(data['msg'] == 'start'):
        msg = {'msg':'start', 'body': random.randint(0,100)}
        emit('updateBabymonitor', msg)
        BabyMonitorController().start_publisher()


@socketio.on('smartphone')
def handle_message(data):
    sleep(1)
    if(data['msg'] == 'start'):
        msg = {'msg':'start', 'body': random.randint(0,100)}
        emit('updateSmartphone', msg)
        SmartphoneController().start_publisher()

