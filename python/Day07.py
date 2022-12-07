
from utils.Stopwatch import runWithStopwatch


def part1():
    commands = open("../input/day07.txt", "r").readlines()
    structure = create_directory_structure(commands)
    total_value = 0
    for value in structure.values():
        if value >= 100000:
            total_value += value
    print("Total memory of big directories are: " + str(total_value))


def create_directory_structure(commands):
    structure = dict()
    directory = ".."
    for command in commands:
        command = command.strip()
        if "$ cd " in command:
            directory = command.split("$ cd ")[1]
            if directory == "..":
                continue
            else:
                structure[directory] = 0
        command = command.split(" ")
        if command[0].isdigit():
            structure[directory] += int(command[0])
    return structure


def part2():
    pass


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
