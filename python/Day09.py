from utils.Stopwatch import runWithStopwatch


def adjacent(dx, dy):
    return abs(dx) <= 1 and abs(dy) <= 1


def sign(val):
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def update_tail(new_head, tail):
    dx = new_head[0] - tail[0]
    dy = new_head[1] - tail[1]
    if not adjacent(dx, dy):
        tail[0] += sign(dx)
        tail[1] += sign(dy)
    return tail


def moveUp(head, tail):
    new_head = [head[0], head[1] + 1]
    tail = update_tail(new_head, tail)
    return new_head, tail


def moveDown(head, tail):
    new_head = [head[0], head[1] - 1]
    tail = update_tail(new_head, tail)
    return new_head, tail


def moveLeft(head, tail):
    new_head = [head[0] - 1, head[1]]
    tail = update_tail(new_head, tail)
    return new_head, tail


def moveRight(head, tail):
    new_head = [head[0] + 1, head[1]]
    tail = update_tail(new_head, tail)
    return new_head, tail


def part1():
    commands = open("../input/day09.txt", "r").readlines()
    tail_position_history = []
    head = [0, 0]
    tail = [0, 0]
    for command in commands:
        command = command.strip().split(" ")
        for i in range(0, int(command[1])):
            match command[0]:
                case "U":
                    head, tail = moveUp(head, tail)
                case "D":
                    head, tail = moveDown(head, tail)
                case "L":
                    head, tail = moveLeft(head, tail)
                case "R":
                    head, tail = moveRight(head, tail)
            tail_position_history.append(tuple(tail))

    print("Number of positions visited at least once: " + str(len(set(tail_position_history))))


def part2():


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
