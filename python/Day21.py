
from utils.Stopwatch import runWithStopwatch


def part1():
    input = open("../input/day21.txt", "r").readlines()
    mapping = dict()
    for line in input:
        l = line.strip().split(": ")
        mapping[l[0]] = Monkey(l[0], l[1], mapping)
    print("Part1: " + str(mapping["root"].shout()))


class Monkey:
    def __init__(self, key, operation: str, mapping):
        self.key = key
        self.operation = operation
        self.mapping = mapping

    def shout(self):
        message = self.operation.split(" ")
        if len(message) > 1:
            return self.execute(message)
        else:
            return int(message[0])

    def execute(self, message):
        match message[1]:
            case '+':
                return self.mapping[message[0]].shout() + self.mapping[message[2]].shout()
            case '-':
                return self.mapping[message[0]].shout() - self.mapping[message[2]].shout()
            case '*':
                return self.mapping[message[0]].shout() * self.mapping[message[2]].shout()
            case '/':
                return self.mapping[message[0]].shout() / self.mapping[message[2]].shout()


def part2():
    input = open("../input/day21.txt", "r").readlines()
    mapping = dict()
    for line in input:
        l = line.strip().split(": ")
        mapping[l[0]] = CorrectMonkey(l[0], l[1], mapping)

    value = 1
    diff = 1
    while not mapping["root"].shout():
        oldvalue = value
        value = value + 1_000_000_000_000
        mapping["humn"] = CorrectMonkey(l[0], str(value), mapping)
        diff = mapping["fgtg"].shout() - mapping["pbtm"].shout() # TODO: Hardcoded correct side to view. This can be generalized.
        if diff < 0:
            leftValue = oldvalue
            rightValue = value
            break

    while not mapping["root"].shout():
        value = int((leftValue + rightValue) / 2)
        mapping["humn"] = CorrectMonkey(l[0], str(value), mapping)
        diff = mapping["fgtg"].shout() - mapping["pbtm"].shout()
        if diff < 0:
            rightValue = value
        else:
            leftValue = value

    print("Part2: " + str(value))

class CorrectMonkey:
    def __init__(self, key, operation: str, mapping):
        self.key = key
        self.operation = operation
        self.mapping = mapping

    def shout(self):
        message = self.operation.split(" ")
        if len(message) > 1:
            return self.execute(message)
        else:
            return int(message[0])

    def execute(self, message):
        if self.key == "root":
            return self.mapping[message[0]].shout() == self.mapping[message[2]].shout()
        match message[1]:
            case '+':
                return self.mapping[message[0]].shout() + self.mapping[message[2]].shout()
            case '-':
                return self.mapping[message[0]].shout() - self.mapping[message[2]].shout()
            case '*':
                return self.mapping[message[0]].shout() * self.mapping[message[2]].shout()
            case '/':
                return self.mapping[message[0]].shout() / self.mapping[message[2]].shout()



if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)