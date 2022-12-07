from utils.Stopwatch import runWithStopwatch

def create_directory_structure(commands):
    directory = Directory("/", None)
    root = directory
    for command in commands:
        command = command.strip()
        if "$ cd " in command:
            directory_name = command.split("$ cd ")[1]
            if directory_name == "..":
                directory = directory.parent
            elif directory_name == "/":
                continue
            else:
                directory = directory.elements[directory_name]
            continue
        command = command.split(" ")
        if command[0].isdigit():
            directory.elements[command[1]] = File(command[1], directory, int(command[0]))
        elif command[0] == "dir":
            directory.elements[command[1]] = Directory(command[1], directory)
    return root





class Element(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def getMemory(self):
        pass


class Directory(Element):
    def __init__(self, name, parent):
        self.elements = dict()
        Element.__init__(self, name, parent)

    def getMemory(self):
        memory: int = 0
        for element in self.elements.values():
            memory += element.getMemory()
        return memory


class File(Element):
    def __init__(self, name, parent, memory: int):
        self.memory = memory
        Element.__init__(self, name, parent)

    def getMemory(self):
        return self.memory


def calculate_total_memory(directory: Directory):
    total_memory = 0
    memory = directory.getMemory()
    if memory <= 100000:
        total_memory += memory

    for element in directory.elements.values():
        if type(element) == Directory(1, 1).__class__:
            total_memory += calculate_total_memory(element)

    return total_memory

def create_list_of_directories(listOfDirectoryMemories, memory_condition: int, directory: Directory):
    memory = directory.getMemory()
    if memory >= memory_condition:
        listOfDirectoryMemories.append(memory)

    for element in directory.elements.values():
        if type(element) == Directory(1, 1).__class__:
            create_list_of_directories(listOfDirectoryMemories, memory_condition, element)



def part1():
    commands = open("../input/day07.txt", "r").readlines()
    root = create_directory_structure(commands)
    total_memory = calculate_total_memory(root)
    print("Total value: " + str(total_memory))

def part2():
    commands = open("../input/day07.txt", "r").readlines()
    root = create_directory_structure(commands)
    max_space = 70000000
    needed_space = 30000000
    root_memory = root.getMemory()
    memory_to_delete = needed_space - (max_space - root_memory)
    listOfDirectories = []
    create_list_of_directories(listOfDirectories, memory_to_delete, root)
    listOfDirectories.sort()
    print("Directory to delete has memeory: " + str(listOfDirectories[0]))


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
