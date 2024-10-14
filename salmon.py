Msg = str
Context = list[Msg]


class Stream:

    def __init__(self):
        self.items = []

    def append(self, msg: Msg):
        self.items.append(msg)

    def context(self, size: int = 0) -> Context:
        return self.items[-size:]


class Scheduler:

    def __init__(self, stream: Stream, *agents: "Agent"):
        self.stream = stream
        self.agents = agents

    def epoch(self) -> Context:
        for ag in self.agents:
            msg = ag.prompt(self.stream.context(ag.context_len))
            if msg is not None:
                self.stream.append(msg)
        return self.stream.context()


class Agent:
    def __init__(self, context_len: int = 1):
        self.context_len = context_len

    def prompt(self, context):
        return None
