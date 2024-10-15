from queue import SimpleQueue
import threading


Msg = str
Context = list[Msg]


class Stream:

    def __init__(self):
        self.items = []

    def append(self, msg: Msg):
        self.items.append(msg)

    @property
    def context(self):
        return self.items


class Scheduler:
    def __init__(self, stream: Stream, *agents: "Agent"):
        self.stream = stream
        self.agents = agents


class RoundRobinScheduler(Scheduler):
    def epoch(self) -> Context:
        for ag in self.agents:
            msg = ag.prompt(self.stream.context)
            if msg is not None:
                self.stream.append(msg)
        return self.stream.context


class ThreadedScheduler(Scheduler):
    def __init__(self, stream: Stream, *agents: "Agent"):
        super().__init__(stream, *agents)
        self.context_q = SimpleQueue()
        self.result_q = SimpleQueue()

        # Create threads
        agent_threads = []
        for ag in self.agents:
            t = threading.Thread(
                target=ag.run,
                daemon=True,
                args=(self.context_q, self.result_q),
            )
            agent_threads.append(t)
            t.start()

        # Bootstrap agents
        for _ in self.agents:
            self.context_q.put(self.stream.context)

    def epoch(self) -> Context:
        msg = self.result_q.get()
        self.stream.append(msg)
        for _ in self.agents:
            self.context_q.put(self.stream.context)
        return self.stream.context


class Agent:
    def prompt(self, context):
        return None

    def run(self, context_q:SimpleQueue, result_q:SimpleQueue):
        while True:
            ctx = context_q.get()
            print(self, 'got', ctx)
            msg = self.prompt(ctx)
            if msg:
                result_q.put(msg)
