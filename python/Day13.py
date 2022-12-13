from utils.Stopwatch import runWithStopwatch


def isCorrectOrder(left, right, withLeftRetry = False, withRightRetry = False):
    for i in range(0, len(left)):
        lefty = left[0] if withLeftRetry else left[i]
        if not withRightRetry and i == len(right):
            return False
        righty = right[0] if withRightRetry else right[i]
        if isinstance(lefty, int) and isinstance(righty, int):
            if lefty > righty:
                return False
            elif lefty < righty:
                return True
        elif isinstance(lefty, list) and isinstance(righty, list):
            if not isCorrectOrder(lefty, righty):
                return False
        elif isinstance(lefty, list) and isinstance(righty, int):
            if not isCorrectOrder(lefty, [righty], withRightRetry=True):
                return False
        elif isinstance(lefty, int) and isinstance(righty, list):
            if not isCorrectOrder([lefty], righty, withLeftRetry=True):
                return False
    return True


def parse(line):
    packet = []
    number = ''
    jump_to = 0
    for i in range(1, len(line)):
        char = line[i]
        if i <= jump_to:
            continue
        match char:
            case "[":
                list_entity, j = parse(line[i:])
                packet.append(list_entity)
                jump_to = i + j
            case "]":
                if number != '':
                    packet.append(int(number))
                return packet, i
            case ",":
                if number == '':
                    continue
                packet.append(int(number))
                number = ''
            case _:
                number += char
    return packet, i


def part1():
    text_input = open("../input/day13.txt", "r").readlines()
    correctPairs = []
    pair = 0
    for i in range(0, len(text_input), 3):
        pair += 1
        left = text_input[i]
        left, _ = parse(left.strip())
        right = text_input[i + 1]
        right, _ = parse(right.strip())
        if isCorrectOrder(left, right):
            correctPairs.append(pair)
    print("Part1: " + str(sum(correctPairs)))


if __name__ == '__main__':
    runWithStopwatch(part1)
