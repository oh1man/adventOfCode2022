from utils.Stopwatch import runWithStopwatch


def compare(left, right):
    # If integers, left < right
    # If lists, left.size <= right.size
    # If list and integer => make integer to list and run list comparison
    pass


def parse(line):
    packet = []
    number = ''
    jump_to = 0
    for i in range(1, len(line) - 1):
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
                    number = ''
                return packet, i
            case ",":
                if number == '':
                    continue
                packet.append(int(number))
                number = ''
            case _:
                number += char
    return packet


def part1():
    text_input = open("../input/day13.txt", "r").readlines()
    for i in range(0, len(text_input), 3):
        left = text_input[i]
        left, _ = parse(left)
        right = text_input[i + 1]
        right, _ = parse(right)
        if compare(left, right):
            pass


if __name__ == '__main__':
    runWithStopwatch(part1)
