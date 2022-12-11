from math import floor

from utils.Stopwatch import runWithStopwatch


def execute_round(monkeys, with_worry):
    for monkey in monkeys:
        monkey.execute(with_worry)


def parse(text_monkeys):
    list_of_monkeys = []
    for monkey in text_monkeys:
        starting_items = [int(item) for item in monkey[0].strip().split("Starting items: ")[1].split(",")]
        operation = monkey[1].strip().split("Operation:")[1].split(" = ")[1]
        divisible_factor = int(monkey[2].strip().split(" by ")[1])
        throw_if_true = int(monkey[3].strip().split(" monkey ")[1])
        throw_if_false = int(monkey[4].strip().split(" monkey ")[1])
        list_of_monkeys.append(
            Monkey(starting_items, operation, divisible_factor, throw_if_true, throw_if_false, list_of_monkeys))
    return list_of_monkeys


def part1():
    text_input = open("../input/day11.txt").readlines()
    text_monkeys = [text_input[i + 1:i + 6] for i in range(0, len(text_input), 7)]
    monkeys = parse(text_monkeys)
    for i in range(0, 20):
        execute_round(monkeys, with_worry=True)

    activity = []
    for monkey in monkeys:
        activity.append(monkey.inspectingCounter)

    activity.sort(reverse=True)
    monkey_business = activity[0] * activity[1]
    print("Part1: " + str(monkey_business))


def part2():
    text_input = open("../input/day11_test.txt").readlines()
    text_monkeys = [text_input[i + 1:i + 6] for i in range(0, len(text_input), 7)]
    monkeys = parse(text_monkeys)
    commonDiv = 1
    for monkey in monkeys:
        commonDiv *= monkey.dividing_factor
    for monkey in monkeys:
        monkey.updateDividor(commonDiv)

    for i in range(0, 10_000):
        execute_round(monkeys, with_worry=False)

    activity = []
    for monkey in monkeys:
        activity.append(monkey.inspectingCounter)

    activity.sort(reverse=True)
    monkey_business = activity[0] * activity[1]
    print("Part2: " + str(monkey_business))


class Monkey:
    def __init__(self, starting_items, operation, dividing_factor, throw_if_true, throw_if_false, family):
        self.items = starting_items
        self.operation = operation
        self.dividing_factor = dividing_factor
        self.throw_if_true = throw_if_true
        self.throw_if_false = throw_if_false
        self.family = family
        self.inspectingCounter = 0
        self.dividor = 3

    def execute(self, with_worry):
        for item in self.items:
            new_item = self.inspect(item)
            new_item = self.bored(new_item, with_worry)
            self.throw(new_item)
        self.items = []

    def inspect(self, item):
        old = item
        self.inspectingCounter += 1
        return eval(self.operation)

    def bored(self, item, with_worry):
        return floor(item / self.dividor)

    def throw(self, item):
        if item % self.dividing_factor == 0:
            self.family[self.throw_if_true].catch(item)
        else:
            self.family[self.throw_if_false].catch(item)

    def catch(self, item):
        self.items.append(item)

    def updateDividor(self, commonDiv):
        self.dividor = commonDiv


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
