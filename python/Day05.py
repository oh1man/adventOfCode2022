from utils.Stopwatch import runWithStopwatch

text_input = open("../input/day05.txt", "r").readlines()


def part1():
    commands, stacks = parse()
    execute_commands(stacks, commands, crateMover9000)
    print(get_top_crates(stacks))


def part2():
    commands, stacks = parse()
    execute_commands(stacks, commands, crateMover9001)
    print(get_top_crates(stacks))


def parse():
    cutoff_index = text_input.index("\n")
    stacks_input = text_input[:cutoff_index]
    stacks = parseStacks(cutoff_index, stacks_input)
    commands = text_input[cutoff_index + 1:]
    return commands, stacks


def parseStacks(cutoff_index, stacks_input):
    parsing_indexes = range(1, len(stacks_input[0]), 4)
    stacks = []
    for line_index in range(cutoff_index - 1, 0 - 1, -1):
        if line_index == cutoff_index - 1:
            for _ in parsing_indexes:
                stacks.append([])
            continue
        i = 0
        for index in parsing_indexes:
            line = stacks_input[line_index]
            crate = line[index]
            if crate != " ":
                stacks[i].append(crate)
            i += 1
    return stacks


def execute_commands(stacks, commands, execute_func):
    for i in range(0, len(commands)):
        command = commands[i].strip()
        start_index = command.index("move ") + len("move ")
        end_index = command.index(" from ")
        move = command[start_index:end_index]
        start_index = end_index + len(" from ")
        end_index = command.index(" to ")
        from_ = command[start_index:end_index]
        start_index = end_index + len(" to ")
        to = command[start_index:]
        execute_func(stacks, int(from_), int(to), int(move))


def crateMover9000(stacks, from_stack, to_stack, number_of_moving):
    for _ in range(0, number_of_moving):
        moving_crate = stacks[from_stack - 1].pop()
        stacks[to_stack - 1].append(moving_crate)
    return stacks


def crateMover9001(stacks, from_stack, to_stack, number_of_moving):
    moving_crates = []
    for _ in range(0, number_of_moving):
        moving_crates.append(stacks[from_stack - 1].pop())
    for i in range(len(moving_crates) - 1, 0 - 1, -1):
        stacks[to_stack - 1].append(moving_crates[i])
    return stacks


def get_top_crates(stacks):
    top_crates = ""
    for stack in stacks:
        top_crates += stack[len(stack) - 1]
    return top_crates


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
