from collections import deque

from utils.Stopwatch import runWithStopwatch


def part1(text):
    index = charactersBeforeUniqueSequence(text, 4)
    print("Number of characters before unique sequence: " + str(index + 1))


def part2(text):
    index = charactersBeforeUniqueSequence(text, 14)
    print("Number of characters before unique sequence: " + str(index + 1))


def charactersBeforeUniqueSequence(text, number_of_characters):
    queue = deque()
    index = 0
    while True:
        char = text.readline(1)
        queue.append(char)
        if len(queue) > number_of_characters:
            queue.popleft()
            if len(queue) == len(set(queue)):
                break
        index += 1
        if char == "":
            break
    return index


def alt_solution(text_input):
    queue = deque()
    index = 0
    for char in text_input.read():
        queue.append(char)
        if len(queue) > 4:
            queue.popleft()
            if len(queue) == len(set(queue)):
                break
        index += 1
    return index


def alt_solution2(text_input):
    queue = deque()
    for i, char in enumerate(text_input.read()):
        queue.append(char)
        if len(queue) > 4:
            queue.popleft()
            if len(queue) == len(set(queue)):
                return i
    return -1


if __name__ == '__main__':
    runWithStopwatch(lambda: part1(open("../input/day06.txt", "r")))
    runWithStopwatch(lambda: part2(open("../input/day06.txt", "r")))

    # Alternative solutions
    runWithStopwatch(lambda: print("Alt solution: " + str(alt_solution(open("../input/day06.txt", "r")) + 1)))
    runWithStopwatch(lambda: print("Alt solution 2: " + str(alt_solution2(open("../input/day06.txt", "r")) + 1)))
