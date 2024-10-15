'''
Install `typeguard` and run me with:
  pytest --typeguard-packages=salmon
'''
from salmon import Agent, RoundRobinScheduler, ThreadedScheduler, Stream


class TickerAgent(Agent):
    def prompt(self, context):
        return "tick"


class UpperEchoAgent(Agent):
    def prompt(self, context):
        if not context:
            return
        return context[-1].upper()


def test_rr():
    agents = [
        TickerAgent(),
        UpperEchoAgent(),
    ]
    stream = Stream()
    scheduler = RoundRobinScheduler(stream, *agents)
    for _ in range(3):
        ctx = scheduler.epoch()
    assert ctx == ['tick', 'TICK', 'tick', 'TICK', 'tick', 'TICK']


def test_threaded():
    agents = [
        TickerAgent(),
        UpperEchoAgent(),
    ]
    stream = Stream()
    scheduler = ThreadedScheduler(stream, *agents)
    for _ in range(3):
        ctx = scheduler.epoch()
    # Here we can not test for exact result
    assert ctx
    assert all(i in ('tick', 'TICK') for i in ctx)
