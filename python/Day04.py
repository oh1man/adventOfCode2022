from utils.Stopwatch import runWithStopwatch

input_lines = open("../input/day04.txt", "r").readlines()


def part1():
    number_of_overlapping = 0
    for line in input_lines:
        sections = line.strip().split(",")
        first = getRange(sections[0])
        second = getRange(sections[1])
        if first.issubset(second) or second.issubset(first):
            number_of_overlapping += 1
    print("Total number of overlapping: " + str(number_of_overlapping))


def getRange(section):
    ids = section.split("-")
    return set(range(int(ids[0]), int(ids[1]) + 1))


def part2():
    number_of_all_overlapping = 0
    for line in input_lines:
        sections = line.strip().split(",")
        first = getRange(sections[0])
        second = getRange(sections[1])
        if first.intersection(second) or second.intersection(first):
            number_of_all_overlapping += 1
    print("Total number of all overlapping: " + str(number_of_all_overlapping))


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
