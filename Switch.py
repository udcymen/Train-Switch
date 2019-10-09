from Yard import Yard
from States import States
import copy
import time


class Switch:

    def __init__(self, _yard, _start, _end):

        if len(_start.state) != len(_end.state):
            raise Exception("Start State and Goal State Have Different Track Number")

        if len(_start.state) != _yard.num_tracks:
            p

        end_track_position = -1

        for i in range(len(_end.state)):
            if "*" in _end.state[i]:
                end_track_position = i + 1
                break

        if end_track_position == -1:
            raise Exception("Engine Not Found in End State")

        visited = []
        distance = {}
        q = [end_track_position]
        count = 0

        while q:
            _q = []
            for i in range(len(q)):
                if q[i] in visited:
                    continue

                for left, right in _yard.connection:
                    if left == q[i]:
                        _q.append(right)
                    if right == q[i]:
                        _q.append(left)

                visited.append(q[i])
                distance[q[i]] = count
            q = _q
            count += 1

        self.yard = _yard
        self.start = _start
        self.end = _end
        self.end_track_position = end_track_position
        self.distance = distance
        self.found = False
        self.path = None

    # Write a function possible-actions that consumes a Yard (connectivity list) and a State, and
    # produces a list of all actions possible in the given train yard from the given state
    def possible_actions(self, current_state):
        engine_position = current_state.find_engine_state()

        if engine_position == -1:
            raise Exception("Engine Not Found")

        result = []

        for left, right in self.yard.connection:

            if left == right:
                raise Exception("Track Connection Input Error")

            if left == engine_position:
                result.append("right " + str(engine_position) + " " + str(right))
                if len(current_state.state[right - 1]) != 0:
                    result.append("left " + str(right) + " " + str(engine_position))

            if right == engine_position:
                result.append("left " + str(engine_position) + " " + str(left))
                if len(current_state.state[left - 1]) != 0:
                    result.append("right " + str(left) + " " + str(engine_position))

        return result

    # Consumes an Action and a State and produces the new State that
    # will result after actually carrying out the input move in the input state.
    def result(self, action, current_state):
        new_state = copy.deepcopy(current_state)
        action_args = action.split(' ')

        if len(action_args) != 3:
            raise Exception("Action Args Usage: 'string:Direction(left, right) int:source_track int:target_track'")

        if action_args[0] not in ['left', 'right']:
            raise Exception("Invalid State Moving Direction " + action_args[0])

        direction, source, target = action_args[0], int(action_args[1]), int(action_args[2])

        if source is None or target is None:
            raise Exception("Invalid Source or Target Position")

        connected_track = False

        for left, right in self.yard.connection:
            if direction == 'left' and left == target and right == source:
                new_state.move(direction, source, target)
                connected_track = True
                break
            elif direction == 'right' and left == source and right == target:
                new_state.move(direction, source, target)
                connected_track = True
                break

        if not connected_track:
            raise Exception("Source and Target are NOT Connected")

        return new_state

    # Consumes a State and produces a list of all states that
    # can be reached in one Action from the given state.
    def expand(self, current_state):
        result = []
        possible_actions = self.possible_actions(current_state)

        for action in possible_actions:
            result.append(self.result(action, current_state))

        return result

    # Produces a list of Actions that will take the cars in the initial state into the goal state.
    # Use a blind (uninformed) search method. This is a NP Problem. For optimality I use an array
    # to record a set of visited state. Return none if goal state can't be reach.
    def blind_search(self):
        if self.start == self.end:
            return self.start

        visited = [self.start]
        q = self.expand(self.start)

        while q:
            _q = []
            for path in q:
                if path in visited:
                    continue

                if path == self.end:
                    return path

                _q += self.expand(path)
                visited.append(path)

            q = _q

        return None

    # The First Heuristic. Calculate How Many Total Distance of Each Car From End State
    def calculate_heuristic(self, current_state):
        result = 0

        for i in range(len(current_state.state)):
            if i + 1 == self.end_track_position:
                for j in range(1, len(current_state.state[i])):
                    if ord(current_state.state[i][j]) - ord(current_state.state[i][j - 1]) != 1:
                        result += 1
            else:
                result += self.distance[i + 1] * len(current_state.state[i])

        return result

    def dfs(self, path, cost, visited):
        if self.found:
            return

        if len(path) == visited[-1].cost and path[-1] == visited[-1]:
            self.found = True
            self.path = path[:]

        for v in filter(lambda x: x.cost == cost, visited):
            for _p in self.expand(v):
                if _p in visited:
                    path.append(_p)
                    self.dfs(path, cost + 1, visited)
                    path.pop()

    # Search with Heuristic
    def a_star(self):
        if self.start == self.end:
            return self.start

        visited = [self.start]
        q = self.expand(self.start)

        while q:
            q.sort(key=lambda x: x.cost + self.calculate_heuristic(x), reverse=True)
            path = q.pop()
            while path in visited:
                path = q.pop()
            if path == self.end:
                visited.append(path)
                break
            q += self.expand(path)
            visited.append(path)

        self.dfs([], 0, visited)


print("Processing Test Data")

########################################################################
#                                                                      #
#                              Test Data                               #
#                                                                      #
########################################################################
yard = Yard([(1, 2), (1, 3), (3, 5), (4, 5), (2, 6), (5, 6)])
start = States([['*'], ['e'], [], ['b', 'c', 'a'], [], ['d']])
end = States([['*', 'a', 'b', 'c', 'd', 'e'], [], [], [], [], []])
switch = Switch(yard, start, end)

yard2 = Yard([(1, 5), (1, 2), (2, 3), (2, 4)])
start2 = States([['*'], ['d'], ['b'], ['a', 'e'], ['c']])
end2 = States([['*', 'a', 'b', 'c', 'd', 'e'], [], [], [], []])
switch2 = Switch(yard2, start2, end2)

yard3 = Yard([(1, 2), (1, 3)])
start3 = States([['*'], ['a'], ['b']])
end3 = States([['*', 'a', 'b'], [], []])
switch3 = Switch(yard3, start3, end3)

yard4 = Yard([(1, 2), (1, 3), (1, 4)])
start4 = States([['*'], ['a'], ['b', 'c'], ['d']])
end4 = States([['*', 'a', 'b', 'c', 'd'], [], [], []])
switch4 = Switch(yard4, start4, end4)

yard5 = Yard([(1, 2), (1, 3), (1, 4)])
start5 = States([['*'], ['a'], ['c', 'b'], ['d']])  # Note c and b out of order
end5 = States([['*', 'a', 'b', 'c', 'd'], [], [], []])
switch5 = Switch(yard5, start5, end5)

print("Start Testing")
start_time = time.time()

########################################################################
#                                                                      #
#                           Test Possible Path                         #
#                                                                      #
########################################################################
# print(switch.possible_actions(start))
# print(switch2.possible_actions(start2))
# print(switch3.possible_actions(start3))
# print(switch4.possible_actions(start4))
# print(switch5.possible_actions(start5))


########################################################################
#                                                                      #
#                           Test Move Track                            #
#                                                                      #
########################################################################
# print(start)
# print(switch.result("left 2 1", start))
# print(switch.result("right 1 2", start))


########################################################################
#                                                                      #
#                          Test Possible Track                         #
#                                                                      #
########################################################################
# print(start)
# for state in switch.expand(start):
#     print("Possible Tracks for Start: " + str(state))
# print(start2)
# for state in switch2.expand(start2):
#     print("Possible Tracks for Start2 in First Expansion: " + str(state))
#     for next_state in switch2.expand(state):
#         print("Possible Tracks for Start2 in Second Expansion: " + str(next_state))


########################################################################
#                                                                      #
#                    Test Blind(Uninformed) Search                     #
#                                                                      #
########################################################################
# print(switch3.blind_search())
# print(switch4.blind_search())
# print(switch5.blind_search())


########################################################################
#                                                                      #
#                            Test Heuristic                            #
#                                                                      #
########################################################################
# print(start, ". Heuristic value: ", switch.calculate_heuristic(start))
# print(start2, ". Heuristic value: ", switch2.calculate_heuristic(start2))
# print(start3, ". Heuristic value: ", switch3.calculate_heuristic(start3))
# print(start4, ". Heuristic value: ", switch4.calculate_heuristic(start4))
# print(start5, ". Heuristic value: ", switch5.calculate_heuristic(start5))


########################################################################
#                                                                      #
#                            Test A* Search                            #
#                                                                      #
########################################################################
# print("Switch 1: The First Possible Way")
# switch.a_star()
# for p in switch.path:
#     print(p)
# print("Switch 2: The First Possible Way")
# switch2.a_star()
# for p in switch2.path:
#     print(p)
# print("Switch 3: The First Possible Way")
# switch3.a_star()
# for p in switch3.path:
#     print(p)
# print("Switch 4: The First Possible Way")
# switch4.a_star()
# for p in switch4.path:
#     print(p)
# print("Switch 5: The First Possible Way")
# switch5.a_star()
# for p in switch5.path:
#     print(p)


print("--- %s seconds ---" % (time.time() - start_time))


########################################################################
#                                                                      #
#                               A* Result                              #
#                                                                      #
########################################################################
# print(switch.a_star())

# print(switch2.a_star())
# Current State Are [['*', 'a', 'b', 'c', 'd', 'e'], [], [], [], []] with Cost 16
# --- 95.16633439064026 seconds ---


