from project.util.construct_scenario import (exchange)
from project.util.config_broker import ConfigScenario
from threading import Thread


class SmartTvPublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')

    def run(self):
        pass
