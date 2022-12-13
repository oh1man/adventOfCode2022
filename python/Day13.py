from utils.Stopwatch import runWithStopwatch


# TODO LEARNING: Algos fit very well with short names, view it like mathematical functions more than system code.
def ordered(L, R):
    for i in range(0, len(L)):
        if i >= len(R):
            return -1
        l = L[i]
        r = R[i]
        if type(l) is int and type(r) is int:
            if l < r:
                return 1
            elif l > r:
                return -1
        elif type(l) is list and type(r) is list:
            j = ordered(l, r)
            if j != 0:
                return j
        elif type(l) is list:
            j = ordered(l, [r])
            if j != 0:
                return j
        elif type(r) is list:
            j = ordered([l], r)
            if j != 0:
                return j
    if len(L) == len(R):
        return 0
    return 1


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
        left, _ = parse(text_input[i].strip())
        right, _ = parse(text_input[i + 1].strip())
        if ordered(left, right) > 0:
            correctPairs.append(pair)
    print("Part1: " + str(sum(correctPairs)))


def parse_packets(text_input):
    packets = []
    for line in text_input:
        if line == "\n":
            continue
        packet, _ = parse(line.strip())
        packets.append(packet)
    return packets

def part2():
    text_input = open("../input/day13_test.txt", "r").readlines()
    text_input.append("[[6]]")
    text_input.append("[[2]]")
    packets = parse_packets(text_input)
    sorted_packets = packets.copy()
    # Now we need to sort this:
    for i in range(0, len(packets)):
        index = i
        sorting = packets[i]
        for j in range(0, len(packets)):
            target = sorted_packets[j]
            if ordered(sorting, target) < 0:
                sorted_packets[index] = target
                sorted_packets[j] = sorting
                index = j

    decoder_key = sorted_packets.index([[6]]) * sorted_packets.index([[2]])
    print("Part2: " + str(decoder_key))

if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
