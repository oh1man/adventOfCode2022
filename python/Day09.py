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
    for i in range(0, len(tail)):
        tail[i] = update_internal_tail(new_head, tail[i])
        new_head = tail[i]
    return tail


def update_internal_tail(new_head, tail):
    dx = new_head[0] - tail[0]
    dy = new_head[1] - tail[1]
    if not adjacent(dx, dy):
        tail = [tail[0] + sign(dx), tail[1] + sign(dy)]
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
    tail_position_history = move_rope(commands, 1)
    print("Number of positions visited at least once: " + str(len(set(tail_position_history))))


def move_rope(commands, tail_length):
    tail_position_history = []
    head = [0, 0]
    tail = [[0, 0]] * tail_length
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
            tail_position_history.append(tuple(tail[len(tail) - 1]))
    return tail_position_history


def part2():
    commands = open("../input/day09.txt", "r").readlines()
    tail_position_history = move_rope(commands, 9)
    print("Number of positions visited at least once: " + str(len(set(tail_position_history))))

if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)

