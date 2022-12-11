from utils.Stopwatch import runWithStopwatch


def part1():
    text_input = open("../input/day11_test.txt").readlines()


    print("Test")


def part2():
    pass


class Monkey:
    def __init__(self, starting_items, operation, dividing_factor, throw_if_true, throw_if_false, family):
        self.items = starting_items
        self.operation = operation
        self.dividing_factor = dividing_factor
        self.throw_if_true = throw_if_true
        self.throw_if_false = throw_if_false
        self.family = family
        self.inspectingCounter = 0

    def execute(self):
        for item in self.items:
            new_item = self.inspect(item)
            new_item = self.bored(new_item)
            self.bored(new_item)

    def inspect(self, item):
        old = item
        self.inspectingCounter += 1
        return eval(self.operation)

    def bored(self, item):
        return round(item / 3)

    def throw(self, item):
        if item % self.dividing_factor == 0:
            self.family[self.throw_if_true].catch(item)
        else:
            self.family[self.throw_if_false].catch(item)

    def catch(self, item):
        self.items.append(item)


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
