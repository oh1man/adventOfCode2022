from utils.Stopwatch import runWithStopwatch

input = open("../input/day03.txt", "r").readlines()


def part1():
    priority_point = 0
    for line in input:
        stripped_line = line.strip()
        middle_index = int(len(stripped_line) / 2)
        unique_first_compartment = toUniqueList(stripped_line[:middle_index])
        unique_second_compartment = toUniqueList(stripped_line[middle_index:])
        for i in unique_first_compartment:
            for j in unique_second_compartment:
                if i == j:
                    priority_point += toPriority(i)
                    break
    print("Total priority point: " + str(priority_point))


def part2():
    priority_point = 0
    for index in range(int(len(input) / 3)):
        group = input[index * 3:(index + 1) * 3]
        for i in toUniqueList(group[0].strip()):
            for j in toUniqueList(group[1].strip()):
                if i == j:
                    for k in toUniqueList(group[2].strip()):
                        if j == k:
                            priority_point += toPriority(k)
                            break

    print("Total priority point: " + str(priority_point))


def toUniqueList(first_compartment):
    return list(set(first_compartment))


def toPriority(char: chr) -> int:
    return ord(str(char).lower()) - ord("a") + 1 + (26 if str(char).isupper() else 0)


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
