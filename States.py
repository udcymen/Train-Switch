class States:
    def __init__(self, state):

        self.state = state
        self.cost = 0

    # Return the index of engine. If not exist, return -1
    def find_engine_state(self):
        for i in range(len(self.state)):
            if self.state[i].count('*'):
                return i + 1
        return -1

    # Move instance to new position with increment cost
    def move(self, direction, source, target):
        self.cost += 1

        if source > len(self.state) or target > len(self.state):
            raise Exception("Invalid Source or Target Index")

        engine_position = self.find_engine_state()

        if engine_position not in [source, target]:
            raise Exception("Missing Engine in Source and Target")

        if len(self.state[source - 1]) == 0:
            raise Exception("Empty Track. Track No: " + source)

        if direction == 'left':
            self.state[target - 1].append(self.state[source - 1].pop(0))
        else:
            self.state[target - 1].insert(0, self.state[source - 1].pop())

    def __str__(self):
        return "Current State Are " + str(self.state) + " with Cost " + str(self.cost)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if not isinstance(other, States):
            raise Exception("Compare Against Different Class Instance")

        return self.state == other.state

