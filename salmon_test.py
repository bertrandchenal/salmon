from time import sleep
from salmon import Agent, Scheduler, Stream


class TickerAgent(Agent):
    def prompt(self, context):
        return "tick"


class UpperEchoAgent(Agent):
    def prompt(self, context):
        if not context:
            return
        return context[-1].upper()


def test_ticker():
    agents = [
        TickerAgent(),
        UpperEchoAgent(),
    ]
    stream = Stream()
    scheduler = Scheduler(stream, *agents)
    for _ in range(3):
        ctx = scheduler.epoch()
    assert ctx == ['tick', 'TICK', 'tick', 'TICK', 'tick', 'TICK']
